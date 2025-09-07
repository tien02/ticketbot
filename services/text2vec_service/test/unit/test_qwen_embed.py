from src import QwenEmbedder

task = "Given a web search query, retrieve relevant passages that answer the query"
queries = ["What is the capital of China?", "Explain gravity"]
documents = [
    "The capital of China is Beijing.",
    "Gravity is a force that attracts two bodies towards each other.",
]

embedder = QwenEmbedder()

# List of text only
embeddings = embedder.embed(texts=queries)
print("Embeddings shape:", embeddings.shape)

# Text only
embeddings = embedder.embed(texts=queries[0])
print("Embeddings shape:", embeddings.shape)
