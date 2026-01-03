#!/bin/bash
set -e

MODEL_DIR="./Qwen3-0.6B"

# 1. Download Model if not present
if [ ! -d "$MODEL_DIR" ]; then
    echo "Model directory '$MODEL_DIR' not found."
    echo "Downloading Qwen/Qwen3-0.6B to local directory..."
    uv run hf download Qwen/Qwen3-0.6B --local-dir "$MODEL_DIR"
else
    echo "Found local model at: $MODEL_DIR"
fi

echo "Starting Training..."
uv run mlx_lm.lora \
  --model "$MODEL_DIR" \
  --train \
  --data ./data \
  --batch-size 4 \
  --iters 150 \
  --learning-rate 2e-4 \
  --adapter-path adapters \
  --save-every 50 \
  --seed 42

echo "Fusing Model..."
uv run mlx_lm.fuse \
  --model "$MODEL_DIR" \
  --adapter-path adapters \
  --save-path Qwen3-compliance_agent_medical-v1

echo "Training and Fusing Complete."
echo "Starting Compliance Agent CLI..."
uv run python compliance_cli.py
