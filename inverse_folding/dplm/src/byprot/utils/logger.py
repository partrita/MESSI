# Copyright (c) 2024 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: Apache-2.0


from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Union,
)

from lightning.fabric.utilities.types import _PATH
from lightning.pytorch.loggers.logger import Logger
from lightning.pytorch.loggers.wandb import WandbLogger

if TYPE_CHECKING:
    from wandb.sdk.lib import RunDisabled
    from wandb.wandb_run import Run

import os

from lightning.pytorch.callbacks.model_checkpoint import ModelCheckpoint
from lightning.pytorch.utilities.exceptions import MisconfigurationException


class ByProtWandbLogger(WandbLogger):
    def __init__(
        self,
        name: str | None = None,
        save_dir: _PATH = ".",
        version: str | None = None,
        offline: bool = False,
        dir: _PATH | None = None,
        id: str | None = None,
        anonymous: bool | None = None,
        project: str | None = None,
        log_model: Literal["all"] | bool = False,
        experiment: Union["Run", "RunDisabled", None] = None,
        prefix: str = "",
        checkpoint_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        # HIGHLIGHT: Remove this check below
        # if not _WANDB_AVAILABLE:
        #     raise ModuleNotFoundError(str(_WANDB_AVAILABLE))

        if offline and log_model:
            raise MisconfigurationException(
                f"Providing log_model={log_model} and offline={offline} is an invalid configuration"
                " since model checkpoints cannot be uploaded in offline mode.\n"
                "Hint: Set `offline=False` to log your model."
            )

        # super().__init__()
        Logger.__init__(self)
        self._offline = offline
        self._log_model = log_model
        self._prefix = prefix
        self._experiment = experiment
        self._logged_model_time: dict[str, float] = {}
        self._checkpoint_callback: ModelCheckpoint | None = None

        # paths are processed as strings
        if save_dir is not None:
            save_dir = os.fspath(save_dir)
        elif dir is not None:
            dir = os.fspath(dir)

        project = project or os.environ.get("WANDB_PROJECT", "lightning_logs")

        # set wandb init arguments
        self._wandb_init: dict[str, Any] = {
            "name": name,
            "project": project,
            "dir": save_dir or dir,
            "id": version or id,
            "resume": "allow",
            "anonymous": ("allow" if anonymous else None),
        }
        self._wandb_init.update(**kwargs)
        # extract parameters
        self._project = self._wandb_init.get("project")
        self._save_dir = self._wandb_init.get("dir")
        self._name = self._wandb_init.get("name")
        self._id = self._wandb_init.get("id")
        self._checkpoint_name = checkpoint_name
