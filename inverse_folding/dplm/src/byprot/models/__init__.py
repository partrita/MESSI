# Copyright (c) 2024 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: Apache-2.0


import glob  # noqa: F401
import importlib  # noqa: F401
import os

from omegaconf import DictConfig  # noqa: F401

from byprot.utils import import_modules

MODEL_REGISTRY = {}


def register_model(name):
    def decorator(cls):
        MODEL_REGISTRY[name] = cls
        return cls

    return decorator


# automatically import any Python files in the models/ directory
import_modules(
    os.path.dirname(__file__),
    "byprot.models",
    excludes=["protein_structure_prediction", "dplm2"],
)
