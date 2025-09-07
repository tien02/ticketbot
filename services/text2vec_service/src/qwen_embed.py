import logging
from typing import List, Optional, Union

import numpy as np
import torch
import torch.nn.functional as F
from torch import Tensor
from transformers import AutoModel, AutoTokenizer


class QwenEmbedder:
    def __init__(
        self,
        model_name: str = "Qwen/Qwen3-Embedding-0.6B",
        max_length: int = 8192,
        use_flash_attention: bool = False,
        use_half_precision: bool = False,
        device: Union[str, torch.device] = None,
    ):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, padding_side="left")

        model_args = {}
        if use_flash_attention:
            model_args["attn_implementation"] = "flash_attention_2"
        if use_half_precision:
            model_args["torch_dtype"] = torch.float16

        self.model = AutoModel.from_pretrained(model_name, **model_args)
        self.model.eval()

        if device is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.device = device
        self.model.to(self.device)

        self.max_length = max_length

        self.logger = logging.getLogger("ray")

    @staticmethod
    def last_token_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
        left_padding = attention_mask[:, -1].sum() == attention_mask.shape[0]
        if left_padding:
            return last_hidden_states[:, -1]
        else:
            sequence_lengths = attention_mask.sum(dim=1) - 1
            batch_size = last_hidden_states.shape[0]
            return last_hidden_states[
                torch.arange(batch_size, device=last_hidden_states.device),
                sequence_lengths,
            ]

    @staticmethod
    def get_detailed_instruction(task_description: str, query: str) -> str:
        return f"Instruct: {task_description}\nQuery:{query}"

    def embed(
        self,
        texts: Optional[Union[str, List[str]]] = None,
    ) -> np.ndarray:

        if isinstance(texts, str):
            texts = [texts]

        self.logger.info(f"Input text: {texts}")

        batch_dict = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt",
        )
        batch_dict = {k: v.to(self.device) for k, v in batch_dict.items()}
        with torch.no_grad():
            outputs = self.model(**batch_dict)
        embeddings = self.last_token_pool(
            outputs.last_hidden_state, batch_dict["attention_mask"]
        )
        embeddings = F.normalize(embeddings, p=2, dim=1)
        return embeddings.cpu().numpy()

    def score(self, queries: List[str], documents: List[str], task: str) -> np.ndarray:
        query_texts = [self.get_detailed_instruction(task, q) for q in queries]
        all_texts = query_texts + documents
        embeddings = self.embed(texts=all_texts)
        query_embeds = embeddings[: len(queries)]
        candidate_embeds = embeddings[len(queries) :]
        return np.matmul(query_embeds, candidate_embeds.T)
