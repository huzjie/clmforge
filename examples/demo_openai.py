# -*- coding: utf-8 -*-
"""Example: OpenAI-compatible slow backend (config)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from clmforge.backends.factory import make_backend


def main():
    # 接 OpenAI 兼容服务作为慢路径；未配置 base_url 时打印说明
    b = make_backend("openai", base_url="https://api.openai.com/v1",
                     model="gpt-4o-mini")
    print("backend kind:", b.kind)
    print("model:", b.model)
    print("(set CLM_OPENAI_API_KEY to actually call)")


if __name__ == "__main__":
    main()
