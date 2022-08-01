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
# Modified   : Sunday July 31st 2022 09:37:37 pm                                                   #
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
from lcd.utils.log_config import LOG_CONFIG

# ------------------------------------------------------------------------------------------------ #
logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #

# ================================================================================================ #
#                                    TEST SOMETHING                                                #
# ================================================================================================ #


@pytest.mark.config
class TestConfig:
    def test_data_config(self, caplog):
        logger.info("\tStarted {} {}".format(self.__class__.__name__, inspect.stack()[0][3]))
        external = "./data/0_external"
        raw = "./data/1_raw"
        raw_lidc = "./data/1_raw/LIDC-IDRI"
        interim = "./data/2_interim"
        final = "./data/3_final"

        final_images = "./data/2_final/images"
        final_masks = "./data/2_final/masks"

        non_nodule_cases = "./data/0_external/non_nodule_cases.csv"

        include_small_nodules = False
        include_non_nodules = False

        config = DataConfig()
        assert external == config.external_data_folder
        assert raw == config.raw_data_folder
        assert raw_lidc == config.raw_lidc_data_folder
        assert interim == config.interim_data_folder
        assert final == config.final_data_folder

        assert final_images == config.final_images_folder
        assert final_masks == config.final_masks_folder

        assert non_nodule_cases == config.non_nodule_cases

        assert include_small_nodules == config.include_small_nodules
        assert include_non_nodules == config.include_non_nodules

        logger.info("\tCompleted {} {}".format(self.__class__.__name__, inspect.stack()[0][3]))

    def test_pylidc_config(self, caplog):
        logger.info("\tStarted {} {}".format(self.__class__.__name__, inspect.stack()[0][3]))

        confidence_level = 0.5
        padding = 512  # TBD Check maximum bound box dimensions.

        config = PylidcConfig()
        assert confidence_level == config.confidence_level
        assert padding == config.padding

        logger.info("\tCompleted {} {}".format(self.__class__.__name__, inspect.stack()[0][3]))
