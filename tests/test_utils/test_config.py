#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Lung Cancer Detection                                                               #
# Version    : 0.1.0                                                                               #
# Filename   : /test_config.py                                                                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/LungCancerDetection                                #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday July 29th 2022 01:01:20 am                                                   #
# Modified   : Friday July 29th 2022 02:47:20 am                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : BSD 3-clause "New" or "Revised" License                                             #
# Copyright  : (c) 2022 John James                                                                 #
# ================================================================================================ #
import inspect
import pytest
import logging
import logging.config

# Enter imports for modules and classes being tested here
from lcd.utils.config import DataConfig, PylidcConfig

# ------------------------------------------------------------------------------------------------ #
logging.config.fileConfig(fname="config/log.conf")
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #

# ================================================================================================ #
#                                    TEST SOMETHING                                                #
# ================================================================================================ #


@pytest.mark.config
class TestConfig:
    def test_data_config(self, caplog):
        logger.info("\tStarted {} {}".format(self.__class__.__name__, inspect.stack()[0][3]))
        raw = "./data/0_raw/LIDC-IDRI"
        metadata = "./data/1_meta"
        images = "./data/2_final/images"
        masks = "./data/2_final/masks"

        config = DataConfig()
        assert raw == config.raw_data_folder
        assert metadata == config.metadata_folder
        assert images == config.image_folder
        assert masks == config.mask_folder

        logger.info("\tCompleted {} {}".format(self.__class__.__name__, inspect.stack()[0][3]))

    def test_pylidc_config(self, caplog):
        logger.info("\tStarted {} {}".format(self.__class__.__name__, inspect.stack()[0][3]))

        confidence_level = 0.5
        padding = 512  # TBD Check maximum bound box dimensions.

        config = PylidcConfig()
        assert confidence_level == config.confidence_level
        assert padding == config.padding

        logger.info("\tCompleted {} {}".format(self.__class__.__name__, inspect.stack()[0][3]))
