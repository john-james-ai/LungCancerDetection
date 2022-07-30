#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Lung Cancer Detection                                                               #
# Version    : 0.1.0                                                                               #
# Filename   : /config.py                                                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/LungCancerDetection                                #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday July 29th 2022 12:41:04 am                                                   #
# Modified   : Friday July 29th 2022 06:38:57 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : BSD 3-clause "New" or "Revised" License                                             #
# Copyright  : (c) 2022 John James                                                                 #
# ================================================================================================ #
import configparser

# ------------------------------------------------------------------------------------------------ #
DATA_CONFIG = "config/data.conf"
PYLIDC_CONFIG = "config/pylidc.conf"


class DataConfig:
    def __init__(self, config_filepath: str = DATA_CONFIG):
        self._config_filepath = config_filepath
        self._parser = configparser.ConfigParser()
        self._parser.read(config_filepath)

    @property
    def raw_data_folder(self) -> str:
        return self._parser["folders"]["raw"]

    @property
    def image_folder(self) -> str:
        return self._parser["folders"]["images"]

    @property
    def mask_folder(self) -> str:
        return self._parser["folders"]["masks"]

    @property
    def metadata_folder(self) -> str:
        return self._parser["folders"]["metadata"]


class PylidcConfig:
    def __init__(self, config_filepath: str = PYLIDC_CONFIG):
        self._config_filepath = config_filepath
        self._parser = configparser.ConfigParser()
        self._parser.read(config_filepath)

    @property
    def confidence_level(self) -> str:
        return float(self._parser["pylidc"]["confidence_level"])

    @property
    def padding(self) -> str:
        return int(self._parser["pylidc"]["padding"])
