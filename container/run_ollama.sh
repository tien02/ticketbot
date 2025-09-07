#!/bin/sh
set -e

echo "Starting Ollama server..."
ollama serve &

echo "Waiting for Ollama to be ready..."
until ollama list > /dev/null 2>&1; do
  echo "Ollama server not ready yet, waiting..."
  sleep 1
done

echo "Preloading model: $OLLAMA_MODEL_NAME..."
ollama pull "$OLLAMA_MODEL_NAME"

echo "Warming up model with a simple prompt..."
ollama run "$OLLAMA_MODEL_NAME" "Hello" > /dev/null

echo "✅ Ollama with model $OLLAMA_MODEL_NAME is ready and running."

wait
