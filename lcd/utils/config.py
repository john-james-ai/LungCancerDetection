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
# Modified   : Sunday July 31st 2022 11:32:13 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : BSD 3-clause "New" or "Revised" License                                             #
# Copyright  : (c) 2022 John James                                                                 #
# ================================================================================================ #
import configparser

# ------------------------------------------------------------------------------------------------ #
DATA_CONFIG = "config/data.conf"
PYLIDC_CONFIG = "config/pylidc.conf"


class DataConfig:
    def __init__(self, config_filepath=DATA_CONFIG):
        self._config_filepath = config_filepath
        self._parser = configparser.ConfigParser()
        self._parser.read(config_filepath)

    # Folders
    @property
    def external_data_folder(self) -> str:
        return self._parser["folders"]["external"]

    @property
    def raw_data_folder(self) -> str:
        return self._parser["folders"]["raw"]

    @property
    def raw_lidc_data_folder(self) -> str:
        return self._parser["folders"]["raw_lidc"]

    @property
    def interim_data_folder(self) -> str:
        return self._parser["folders"]["interim"]

    @property
    def final_data_folder(self) -> str:
        return self._parser["folders"]["final"]

    @property
    def final_images_folder(self) -> str:
        return self._parser["folders"]["final_images"]

    @property
    def final_masks_folder(self) -> str:
        return self._parser["folders"]["final_masks"]

    # Files
    @property
    def metadata_filepath(self) -> str:
        return self._parser["filepaths"]["metadata"]

    @property
    def non_nodule_cases_filepath(self) -> str:
        return self._parser["filepaths"]["non_nodule_cases"]

    @property
    def cases_filepath(self) -> str:
        return self._parser["filepaths"]["cases"]

    @property
    def annotations_filepath(self) -> str:
        return self._parser["filepaths"]["annotations"]

    @property
    def nodules_filepath(self) -> str:
        return self._parser["filepaths"]["nodules"]

    @property
    def small_nodules_filepath(self) -> str:
        return self._parser["filepaths"]["small_nodules"]

    @property
    def non_nodules_filepath(self) -> str:
        return self._parser["filepaths"]["non_nodules"]


# ------------------------------------------------------------------------------------------------ #
class PylidcConfig:
    def __init__(self, config_filepath=PYLIDC_CONFIG):
        self._config_filepath = config_filepath
        self._parser = configparser.ConfigParser()
        self._parser.read(config_filepath)

    @property
    def confidence_level(self) -> str:
        return float(self._parser["pylidc"]["confidence_level"])

    @property
    def padding(self) -> str:
        return int(self._parser["pylidc"]["padding"])
