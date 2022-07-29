#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Lung Cancer Detection                                                               #
# Version    : 0.1.0                                                                               #
# Filename   : /nodule.py                                                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/LungCancerDetection                                #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday July 27th 2022 03:49:40 pm                                                #
# Modified   : Thursday July 28th 2022 11:49:56 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : BSD 3-clause "New" or "Revised" License                                             #
# Copyright  : (c) 2022 John James                                                                 #
# ================================================================================================ #
import pylidc as pl
import pandas as pd
from typing import Union

# ------------------------------------------------------------------------------------------------ #


class Nodule:
    """The term “nodule” represents a spectrum of abnormalities (irrespective of presumed
    histology), which is itself a subset of a broader spectrum of abnormalities termed
    “focal abnormality;” a lesion should be considered a “nodule” if it
    satisfies the definition of “nodule” (the most essential component of which is its
    "nodular" morphology)

    Args:
        nid (int): An integer between 1 and 6, indicating the unique nodule for a patient.
        pid (str): The patient id in the form of LIDC-IDRI-dddd
    """

    def __init__(self, nid: int, pid: str) -> None:
        self._nid = nid
        self._pid = pid
        self._scan = pl.query(pl.Scan).filter(pl.Scan.patient_id == pid).first()
        self._annotations = self._scan.cluster_annotations()[nid]

    @property
    def annotations(self) -> list:
        return self._annotations

