#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Lung Cancer Detection                                                               #
# Version    : 0.1.0                                                                               #
# Filename   : /log_config.py                                                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/LungCancerDetection                                #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday July 31st 2022 01:51:26 pm                                                   #
# Modified   : Sunday July 31st 2022 03:01:01 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : BSD 3-clause "New" or "Revised" License                                             #
# Copyright  : (c) 2022 John James                                                                 #
# ================================================================================================ #
LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "multiprocess": {
            "format": "%(levelname)s | %(asctime)s | %(module)s | %(process)d  | %(thread)d  | %(message)s"
        },
        "verbose": {"format": "%(levelname)s | %(asctime)s | %(module)s | %(message)s"},
        "standard": {"format": "%(levelname)s | %(asctime)s | %(message)s"},
        "simple": {"format": "%(message)s"},
    },
    "handlers": {
        "console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "simple"},
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "verbose",
            "filename": "logs/lcd.log",
            "when": "D",
            "backupCount": 3,
        },
    },
    "loggers": {"root": {"handlers": ["console", "file"], "propagate": False, "level": "DEBUG"}},
}
