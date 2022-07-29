#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Lung Cancer Detection                                                               #
# Version    : 0.1.0                                                                               #
# Filename   : /lidc.py                                                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/LungCancerDetection                                #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday July 26th 2022 03:35:58 pm                                                  #
# Modified   : Tuesday July 26th 2022 08:52:42 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : BSD 3-clause "New" or "Revised" License                                             #
# Copyright  : (c) 2022 John James                                                                 #
# ================================================================================================ #
import pylidc as pl
from typing import Union

# ------------------------------------------------------------------------------------------------ #


class Patient:
    """Represents a patient object

    Args:
        id (str): String of an integer between 1 and 1012, the number of patients in the LIDC database.

    """

    def __init__(self, id: str) -> None:
        self._pid = self._format_patient_id(id)
        self._scan = pl.query(pl.Scan).filter(pl.Scan.patient_id == self._pid).first()
        self._annotations = {}
        self._clustered_annotations = None
        self._annotation_count = None
        self._nodule_count = None

    @property
    def pid(self) -> str:
        return self._pid

    @property
    def scan(self) -> pl.Scan:
        return self._scan

    @property
    def nodules(self) -> Union[list]:
        """Returns a list of dictionaries, each entry a nodule, annotation pair."""
        if self._annotation_count is None:
            self._annotation_count = len(self.annotations())
        return self._annotation_count

    def annotations(self, nodule: int = None) -> Union[dict, list]:
        """Returns annotation for a nodule or all nodules (if nodules is None)

        Args:
            nodule (int): The nodule number

        Returns:
            Union[dict,list]

        """
        if not self._annotations:
            for i, annotation in enumerate(self._scan.cluster_annotations()):
                self._annotations[i + 1] = annotation
        if not nodule:
            return self._annotations
        else:
            return self._annotations[nodule]

    def visualize(self) -> None:
        """Returns the CT Scan for the patient."""
        if not self._clustered_annotations:
            self._clustered_annotations = self._scan.cluster_annotations()
        self._scan.visualize(annotation_groups=self._clustered_annotations)

    def _format_patient_id(self, id) -> str:
        """Returns a patient id in form of "LIDC-IDRI-dddd'"""
        return "LIDC-IDRI-" + id.zfill(4)
