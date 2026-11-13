# Copyright (c) 2024 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: Apache-2.0


import glob  # noqa: F401
import importlib  # noqa: F401
import os

from omegaconf import DictConfig  # noqa: F401

from byprot.utils import import_modules

DATAMODULE_REGISTRY = {}


def register_datamodule(name):
    def decorator(cls):
        DATAMODULE_REGISTRY[name] = cls
        return cls

    return decorator


import_modules(os.path.dirname(__file__), "byprot.datamodules")
