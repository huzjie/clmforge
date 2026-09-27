# -*- coding: utf-8 -*-
"""Example: retrieval re-ranking."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from clmforge.models.clm_model import CLMModel
from clmforge.integrations.retrieval_rerank import rerank


def main():
    model = CLMModel()
    docs = [
        "Python is a programming language",
        "PyTorch is a deep learning framework",
        "Git is a version control system",
        "Docker is a container runtime",
        "Kubernetes orchestrates containers",
    ]
    for q in ["machine learning tools", "shipping code", "running services at scale"]:
        print(f"query: {q!r}")
        for doc, score in rerank(model, q, docs, top_n=3):
            print(f"   {score:.3f}  {doc}")


if __name__ == "__main__":
    main()
