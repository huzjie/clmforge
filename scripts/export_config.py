# -*- coding: utf-8 -*-
"""Export the effective config to JSON (handy for debugging)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from clmforge.config import load_config


def main():
    cfg = load_config("config.yaml")
    cfg.save_json("config.exported.json")
    print("saved config.exported.json")


if __name__ == "__main__":
    main()
