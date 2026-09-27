# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="clmforge",
    version="1.0.0",
    description="Contrastive Language Model for fast decision-making",
    packages=find_packages(include=["clmforge", "clmforge.*"]),
    python_requires=">=3.9",
    entry_points={"console_scripts": ["clmforge=clmforge.cli:main"]},
)
