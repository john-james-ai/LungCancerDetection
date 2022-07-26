#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Lung Cancer Detection                                                               #
# Version    : 0.1.0                                                                               #
# Filename   : /__init__.py                                                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/LungCancerDetection                                #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday July 26th 2022 03:34:05 pm                                                  #
# Modified   : Sunday July 31st 2022 01:41:41 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : BSD 3-clause "New" or "Revised" License                                             #
# Copyright  : (c) 2022 John James                                                                 #
# ================================================================================================ #
import logging

# ------------------------------------------------------------------------------------------------ #
#                                           LOGGING                                                #
# ------------------------------------------------------------------------------------------------ #
# Handlers
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
file_handler = logging.handlers.TimedRotatingFileHandler(
    filename="logs/lcd.log", when="D", interval=1, backupCount=3
)
file_handler.setLevel(logging.DEBUG)
# ------------------------------------------------------------------------------------------------ #
# Formatters
format = "%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s"
# ------------------------------------------------------------------------------------------------ #
# Config
logging.basicConfig(level=logging.DEBUG, format=format, handlers=[file_handler, console_handler])
# ------------------------------------------------------------------------------------------------ #
