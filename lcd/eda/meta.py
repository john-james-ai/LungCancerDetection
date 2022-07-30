#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Lung Cancer Detection                                                               #
# Version    : 0.1.0                                                                               #
# Filename   : /meta.py                                                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/LungCancerDetection                                #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday July 27th 2022 03:49:40 pm                                                #
# Modified   : Friday July 29th 2022 10:30:47 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : BSD 3-clause "New" or "Revised" License                                             #
# Copyright  : (c) 2022 John James                                                                 #
# ================================================================================================ #
import os
import math
import pylidc as pl
import pandas as pd
import numpy as np
from tqdm import tqdm
import logging
import logging.config

from lcd.utils.config import DataConfig
from lcd import ANNOTATION_COLUMNS, NODULE_COLUMNS

# ------------------------------------------------------------------------------------------------ #
logging.config.fileConfig(fname="config/log.conf")
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #


class LIDCMetadata:
    """Extracts and saves LICD annotation and nodule data for analysis..

    Args:
        excluded_patients (dict): Dictionary containing the excluded patients and reason for exclusion.
        force (bool): Specifies whether build is to run if the metadata already exists. If True, build
            will overwrite the existing data. Otherwise, build will only execute if no existing data.
    """

    def __init__(
        self, included_patients: list = [], excluded_patients: dict = {}, force: bool = False
    ) -> None:
        self._included_patients = included_patients
        self._excluded_patients = pd.DataFrame.from_dict(data=excluded_patients, orient="columns")
        self._force = force

        self._annotation_filepath = os.path.join(DataConfig().metadata_folder, "annotations.csv")
        self._nodule_filepath = os.path.join(DataConfig().metadata_folder, "nodules.csv")

        self._annotation_data = pd.DataFrame(index=[], columns=ANNOTATION_COLUMNS["column"].values)
        self._nodule_data = pd.DataFrame(index=[], columns=NODULE_COLUMNS["column"].values)

        if self._exists(self._annotation_filepath) and not self._force:
            self._annotation_data = self._load(self._annotation_filepath)
        if self._exists(self._nodule_filepath) and not self._force:
            self._nodule_data = self._load(self._nodule_filepath)

    def build(self) -> None:
        """Builds the scan metadata to the annotation level."""

        self._build_annotation_data()
        self._build_nodule_data()

    @property
    def scan_count(self) -> int:
        return len(self._annotation_data["patient_id"].unique())

    @property
    def nodule_count(self) -> int:
        return self._nodule_data.shape[0]

    @property
    def annotation_count(self) -> int:
        return self._annotation_data.shape[0]

    @property
    def excluded_patients(self) -> pd.DataFrame:
        return self._excluded_patients

    def _build_annotation_data(self) -> None:
        """Builds the annotation data."""

        # Checks for existence of data vis-a-vis the force parameter
        if self._proceed(self._annotation_filepath):

            scans = self._get_scans()
            print(scans.count())
            with tqdm(total=scans.count()) as pbar:
                # Process clustered annotations by scan
                for scan in scans:

                    pbar.set_description("Processing patient {}".format(scan.patient_id))
                    logger.debug("Processing patient {}".format(scan.patient_id))

                    nodules = scan.cluster_annotations(verbose=False)

                    for nodule_no, nodule in enumerate(nodules):
                        for annotation_no, annotation in enumerate(nodule):

                            # Formats the metadata extracted from the annotation into a list
                            annotation_data = [scan.patient_id, nodule_no, annotation_no]
                            # Extracts the characteristics using the annotation feature_vals method
                            values, semantics = annotation.feature_vals(return_str=True)
                            # Adds the nodule characteristics (values and semantic descriptions) to annotation data
                            for value, semantic in zip(values, semantics):
                                annotation_data.append(value)
                            # Add size variables.
                            annotation_data.append(annotation.diameter)
                            annotation_data.append(annotation.volume)
                            annotation_data.append(annotation.surface_area)
                            # Append the data to the annotation DataFrame
                            annotation_dict = {}
                            for i, value in enumerate(ANNOTATION_COLUMNS["column"].values):
                                annotation_dict[ANNOTATION_COLUMNS["column"].values[i]] = []
                                annotation_dict[ANNOTATION_COLUMNS["column"].values[i]].append(
                                    annotation_data[i]
                                )
                            df = pd.DataFrame(annotation_dict, index=[0])
                            self._annotation_data = pd.concat(
                                [self._annotation_data, df], axis=0, ignore_index=True
                            )
                    pbar.update(1)
            self._save(self._annotation_data, self._annotation_filepath)

    def _build_nodule_data(self) -> None:

        if self._proceed(self._nodule_filepath):

            self._nodule_data = (
                self._annotation_data.groupby(["patient_id", "nodule_no"])
                .agg(
                    {
                        "annotation_no": "count",
                        "subtlety": lambda x: math.ceil(np.median(x)),
                        "internalStructure": lambda x: x.value_counts().index[0],
                        "calcification": lambda x: x.value_counts().index[0],
                        "sphericity": lambda x: x.value_counts().index[0],
                        "margin": lambda x: math.ceil(np.median(x)),
                        "lobulation": lambda x: math.ceil(np.median(x)),
                        "spiculation": lambda x: math.ceil(np.median(x)),
                        "texture": lambda x: x.value_counts().index[0],
                        "malignancy": lambda x: math.ceil(np.median(x)),
                        "diameter": "mean",
                        "volume": "mean",
                        "surface_area": "mean",
                    }
                )
                .reset_index()
            )
            self._save(self._nodule_data, self._nodule_filepath)

    def _proceed(self, filepath: str) -> bool:
        """Proceed unless the file exists and force is False."""
        proceed = True

        if os.path.exists(filepath) and not self._force:
            logging.info(
                "Build {} not executed as {} already exists and force is False.".format(
                    os.path.splitext(os.path.basename(filepath))[0], os.path.basename(filepath)
                )
            )
            proceed = False

        return proceed

    def _get_scans(self) -> list:
        if len(self._included_patients) > 0 and self._excluded_patients.shape[0] > 0:
            scans = pl.query(pl.Scan).filter(
                pl.Scan.patient_id.not_in(self._excluded_patients["patient_id"].values),
                pl.Scan.patient_id.in_(self._included_patients),
            )
        elif len(self._included_patients) > 0:
            scans = pl.query(pl.Scan).filter(pl.Scan.patient_id.in_(self._included_patients))
        elif self._excluded_patients.shape[0] > 0:
            scans = pl.query(pl.Scan).filter(
                pl.Scan.patient_id.not_in(self._excluded_patients["patient_id"].values)
            )
        else:
            scans = pl.query(pl.Scan)
        return scans

    def _load(self, filepath: str) -> pd.DataFrame:
        """Loads existing metadata if it exists."""
        if os.path.exists(filepath):
            return pd.read_csv(filepath, engine="pyarrow")

    def _save(self, data: pd.DataFrame, filepath: str) -> None:
        """Saves the metadata to the filepath designated at instantiation."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        data.to_csv(filepath, header=True, index=False)

    def _exists(self, filepath) -> bool:
        """Returns True if metadata already exists, either in memory or on file."""
        return os.path.exists(filepath)
