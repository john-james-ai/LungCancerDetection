#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Lung Cancer Detection                                                               #
# Version    : 0.1.0                                                                               #
# Filename   : /data.py                                                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/LungCancerDetection                                #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday July 27th 2022 03:49:40 pm                                                #
# Modified   : Monday August 1st 2022 03:34:40 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : BSD 3-clause "New" or "Revised" License                                             #
# Copyright  : (c) 2022 John James                                                                 #
# ================================================================================================ #
import os
import inspect
import math
import logging
import logging.config
import pylidc as pl
import pandas as pd
import numpy as np
from tqdm import tqdm
from typing import Tuple


from lcd.utils.config import DataConfig
from lcd.eda import (
    ANNOTATION_COLUMNS,
    NODULE_COLUMNS,
    FEATURE_COLUMNS,
    SMALL_NODULE_COLUMNS,
    CASE_COLUMNS,
)
from lcd.utils.log_config import LOG_CONFIG

# ------------------------------------------------------------------------------------------------ #
logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #


class LIDCData:
    """Extracts and saves LICD annotation and nodule data for analysis..

    Args:
        include_patients (list): A list of patient_ids to use.
        excluded_patients (dict): Dictionary containing the excluded patients and reason for exclusion.
        use_existing_data (bool): If True, the class loads existing annotation and nodule
            data if it exists. Otherwise, the build process proceeds as normal.
    """

    def __init__(
        self,
        included_patients: list = [],
        excluded_patients: dict = {},
        use_existing_data: bool = False,
    ) -> None:
        self._included_patients = included_patients
        self._excluded_patients = excluded_patients
        self._use_existing_data = use_existing_data

        # Input: Reference data including non-nodule cases and metadata
        self._non_nodule_cases = None
        self._non_nodule_cases_filepath = DataConfig().non_nodule_cases_filepath
        self._metadata = None
        self._metadata_filepath = DataConfig().metadata_filepath

        # Output: Filepaths
        self._cases_filepath = DataConfig().cases_filepath
        self._annotations_filepath = DataConfig().annotations_filepath
        self._nodules_filepath = DataConfig().nodules_filepath
        self._small_nodules_filepath = DataConfig().small_nodules_filepath
        self._non_nodules_filepath = DataConfig().non_nodules_filepath

        # Output: Datasets
        self._case_data = pd.DataFrame(index=[], columns=CASE_COLUMNS)
        self._annotation_data = pd.DataFrame(index=[], columns=ANNOTATION_COLUMNS)
        self._nodule_data = pd.DataFrame(index=[], columns=NODULE_COLUMNS)
        self._non_nodule_data = pd.DataFrame(index=[], columns=NODULE_COLUMNS)
        self._small_nodule_data = pd.DataFrame(index=[], columns=SMALL_NODULE_COLUMNS)

    def build(self) -> None:
        """Builds the scan metadata to the annotation level."""
        logger.debug("\tStarted {} {}".format(self.__class__.__name__, inspect.stack()[0][3]))

        if self._use_existing_data and self._data_exists:
            self._load_existing_data()

        else:
            self._load_reference_data()
            self._build_annotation_data()
            self._build_nodule_data()
            # self._build_case_data()
            self._save_data()

        logger.debug("\tCompleted {} {}".format(self.__class__.__name__, inspect.stack()[0][3]))

    def _data_exists(self) -> bool:
        return (
            os.path.exists(self._annotations_filepath)
            and os.path.exists(self._nodules_filepath)
            and os.path.exists(self._small_nodules_filepath)
            and os.path.exists(self._non_nodules_filepath)
        )

    def _load_existing_data(self) -> None:
        logger.info("Loading existing data...")
        # self._case_data = pd.read_csv(self._cases_filepath)
        self._annotation_data = pd.read_csv(self._annotations_filepath)
        self._nodule_data = pd.read_csv(self._nodules_filepath)
        self._small_nodule_data = pd.read_csv(self._small_nodules_filepath)
        self._non_nodule_data = pd.read_csv(self._non_nodules_filepath)

    def _load_reference_data(self) -> None:
        """Loads cases with non or small nodules."""
        self._non_nodule_cases = list(
            pd.read_csv(self._non_nodule_cases_filepath)["patient_id"].values
        )
        self._metadata = pd.read_csv(self._metadata_filepath)

    def _build_annotation_data(self) -> None:
        """Builds the annotation data."""

        logger.debug("\tStarted {} {}".format(self.__class__.__name__, inspect.stack()[0][3]))

        scans = self._get_scans()
        with tqdm(total=scans.count()) as pbar:
            # Process clustered annotations by scan
            for scan in scans:

                pbar.set_description("Processing patient {}".format(scan.patient_id))
                logger.debug("Processing patient {}".format(scan.patient_id))

                nodules = scan.cluster_annotations(verbose=False)

                if len(nodules) == 0:
                    self._create_small_nodule_annotation(scan)
                else:
                    self._create_nodule_annotations(scan, nodules)

                pbar.update(1)

        logger.debug("\tCompleted {} {}".format(self.__class__.__name__, inspect.stack()[0][3]))

    def _create_small_nodule_annotation(self, scan: pl.Scan) -> None:
        """Creates an annotation for a nodule designated to be less than 3mm in diameter."""

        logger.debug("\tStarted {} {}".format(self.__class__.__name__, inspect.stack()[0][3]))

        features = SemanticFeatures()
        df = pd.DataFrame(index=[], columns=ANNOTATION_COLUMNS)
        df["patient_id"] = [scan.patient_id]
        df["scan_id"] = [scan.id]
        df["nodule_classification"] = ["small nodule"]
        df["nodule_id"] = [scan.patient_id + "-" + str(0)]
        df["malignancy"] = [1]
        df["Malignancy"] = [str(1) + "-" + features.Malignancy(1)]
        df["diameter"] = ["<3mm"]
        df["diagnosis"] = ["Benign"]

        self._small_nodule_data = pd.concat(
            [self._small_nodule_data, df], axis=0, ignore_index=True
        )

        logger.debug("\tCompleted {} {}".format(self.__class__.__name__, inspect.stack()[0][3]))

    def _create_nodule_annotations(self, scan: pl.Scan, nodules: list) -> None:
        """Creates annotations for each nodule"""

        logger.debug("\tStarted {} {}".format(self.__class__.__name__, inspect.stack()[0][3]))

        features = SemanticFeatures()

        for nodule_no, nodule in enumerate(nodules, start=1):
            nodule_id = scan.patient_id + "_" + str(nodule_no)

            for annotation_no, annotation in enumerate(nodule, start=1):

                classification, diagnosis = self._get_nodule_designation(annotation)

                df = pd.DataFrame(columns=ANNOTATION_COLUMNS)
                df["patient_id"] = [scan.patient_id]
                df["scan_id"] = [scan.id]
                df["nodule_classification"] = [classification]
                df["nodule_id"] = [nodule_id]
                df["annotation_no"] = [annotation_no]
                df["annotation_id"] = [annotation.id]
                df["n_readers"] = [len(nodule)]
                df["diameter"] = [annotation.diameter]
                df["volume"] = [annotation.volume]
                df["surface_area"] = [annotation.surface_area]
                df["diagnosis"] = [diagnosis]
                df["slice_thickness"] = [annotation.scan.slice_thickness]
                df["slice_spacing"] = [annotation.scan.slice_spacing]
                df["pixel_spacing"] = [annotation.scan.pixel_spacing]

                df["Subtlety"] = [
                    str(annotation.subtlety) + "-" + features.Subtlety(annotation.subtlety)
                ]

                df["InternalStructure"] = [
                    str(annotation.internalStructure)
                    + "-"
                    + features.InternalStructure(annotation.internalStructure)
                ]
                df["Calcification"] = [
                    str(annotation.calcification)
                    + "-"
                    + features.Calcification(annotation.calcification)
                ]
                df["Sphericity"] = [
                    str(annotation.sphericity) + "-" + features.Sphericity(annotation.sphericity)
                ]
                df["Margin"] = [str(annotation.margin) + "-" + features.Margin(annotation.margin)]
                df["Lobulation"] = [
                    str(annotation.lobulation) + "-" + features.Lobulation(annotation.lobulation)
                ]
                df["Spiculation"] = [
                    str(annotation.spiculation) + "-" + features.Spiculation(annotation.spiculation)
                ]
                df["Texture"] = [
                    str(annotation.texture) + "-" + features.Texture(annotation.texture)
                ]
                df["Malignancy"] = [
                    str(annotation.malignancy) + "-" + features.Malignancy(annotation.malignancy)
                ]

                for name, value in zip(FEATURE_COLUMNS, annotation.feature_vals()):
                    df[name] = [value]

                self._annotation_data = pd.concat(
                    [self._annotation_data, df], axis=0, ignore_index=True
                )

        logger.debug("\tCompleted {} {}".format(self.__class__.__name__, inspect.stack()[0][3]))

    def _get_nodule_designation(self, annotation: pl.Annotation) -> Tuple[str, str]:
        """Returns the nodule classification and diagnosis"""
        classification = "nodule"
        if annotation.scan.patient_id in self._non_nodule_cases:
            classification = "non_nodule"
            diagnosis = "Benign"
        else:
            diagnosis = "Malignant" if annotation.malignancy > 3 else "Benign"

        return classification, diagnosis

    def _build_nodule_data(self) -> None:

        logger.debug("\tStarted {} {}".format(self.__class__.__name__, inspect.stack()[0][3]))

        self._nodule_data = self._extract_nodule_data(
            self._annotation_data[self._annotation_data["nodule_classification"] == "nodule"]
        )
        self._non_nodule_data = self._extract_nodule_data(
            self._annotation_data[self._annotation_data["nodule_classification"] == "non_nodule"]
        )

        logger.debug("\tCompleted {} {}".format(self.__class__.__name__, inspect.stack()[0][3]))

    def _extract_nodule_data(self, annotation_data: pd.DataFrame) -> pd.DataFrame:
        """Extracts and aggregates nodule and non-nodule data from the annotation data frame."""

        logger.debug("\tStarted {} {}".format(self.__class__.__name__, inspect.stack()[0][3]))

        nodule_data = (
            annotation_data.groupby(["patient_id", "scan_id", "nodule_id", "nodule_classification"])
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
                    "diagnosis": lambda x: x.value_counts().index[0],
                }
            )
            .rename(columns={"annotation_no": "n_readers"})
            .reset_index()
        )
        features = SemanticFeatures()
        nodule_data["Subtlety"] = [features.Subtlety(x) for x in nodule_data["subtlety"]]
        nodule_data["InternalStructure"] = [
            features.InternalStructure(x) for x in nodule_data["internalStructure"]
        ]

        nodule_data["Calcification"] = [
            features.Calcification(x) for x in nodule_data["calcification"]
        ]

        nodule_data["Sphericity"] = [features.Sphericity(x) for x in nodule_data["sphericity"]]
        nodule_data["Margin"] = [features.Margin(x) for x in nodule_data["margin"]]
        nodule_data["Lobulation"] = [features.Lobulation(x) for x in nodule_data["lobulation"]]
        nodule_data["Spiculation"] = [features.Spiculation(x) for x in nodule_data["spiculation"]]
        nodule_data["Texture"] = [features.Texture(x) for x in nodule_data["texture"]]
        nodule_data["Malignancy"] = [features.Malignancy(x) for x in nodule_data["malignancy"]]

        logger.debug("\tCompleted {} {}".format(self.__class__.__name__, inspect.stack()[0][3]))

        return nodule_data

    def _build_case_data(self) -> None:
        pass

    def _get_scans(self) -> list:
        if len(self._included_patients) > 0 and len(self._excluded_patients) > 0:
            scans = pl.query(pl.Scan).filter(
                pl.Scan.patient_id.not_in(self._excluded_patients),
                pl.Scan.patient_id.in_(self._included_patients),
            )
        elif len(self._included_patients) > 0:
            scans = pl.query(pl.Scan).filter(pl.Scan.patient_id.in_(self._included_patients))
        elif len(self._excluded_patients) > 0:
            scans = pl.query(pl.Scan).filter(pl.Scan.patient_id.not_in(self._excluded_patients))
        else:
            scans = pl.query(pl.Scan)
        return scans

    def _save_data(self) -> None:
        # self._write(self._case_data, self._cases_filepath)
        self._write(self._annotation_data, self._annotations_filepath)
        self._write(self._nodule_data, self._nodules_filepath)
        self._write(self._small_nodule_data, self._small_nodules_filepath)
        self._write(self._non_nodule_data, self._non_nodules_filepath)

    def _read(self, filepath: str) -> pd.DataFrame:
        """Loads existing metadata if it exists."""
        try:
            return pd.read_csv(filepath, engine="pyarrow")
        except FileNotFoundError as e:
            logger.error("File {} does not exist.\n{}".format(filepath, e))
            raise

    def _write(self, data: pd.DataFrame, filepath: str) -> None:
        """Saves the metadata to the filepath designated at instantiation."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        data.to_csv(filepath, header=True, index=False)

    def _exists(self, filepath) -> bool:
        """Returns True if metadata already exists, either in memory or on file."""
        return os.path.exists(filepath)


# ------------------------------------------------------------------------------------------------ #
#                                  SEMANTIC FEATURES                                               #
# ------------------------------------------------------------------------------------------------ #
class SemanticFeatures:
    def Subtlety(self, s: int):
        """Semantic interpretation of `subtlety` value as string."""
        if s == 0:
            return "NA"
        else:

            assert s in range(1, 6), "Subtlety score {} out of bounds.".format(str(s))
            if s == 1:
                return "Extremely Subtle"
            elif s == 2:
                return "Moderately Subtle"
            elif s == 3:
                return "Fairly Subtle"
            elif s == 4:
                return "Moderately Obvious"
            elif s == 5:
                return "Obvious"

    def InternalStructure(self, s: int):
        """Semantic interpretation of `internalStructure` value as string."""
        if s == 0:
            return "NA"
        else:
            assert s in range(1, 5), "Internal structure score out of bounds."
            if s == 1:
                return "Soft Tissue"
            elif s == 2:
                return "Fluid"
            elif s == 3:
                return "Fat"
            elif s == 4:
                return "Air"

    def Calcification(self, s: int):
        """Semantic interpretation of `calcification` value as string."""
        if s == 0:
            return "NA"
        else:
            assert s in range(1, 7), "Calcification score out of bounds."
            if s == 1:
                return "Popcorn"
            elif s == 2:
                return "Laminated"
            elif s == 3:
                return "Solid"
            elif s == 4:
                return "Non-central"
            elif s == 5:
                return "Central"
            elif s == 6:
                return "Absent"

    def Sphericity(self, s: int):
        """Semantic interpretation of `sphericity` value as string."""
        if s == 0:
            return "NA"
        else:
            assert s in range(1, 6), "Sphericity score out of bounds."
            if s == 1:
                return "Linear"
            elif s == 2:
                return "Ovoid/Linear"
            elif s == 3:
                return "Ovoid"
            elif s == 4:
                return "Ovoid/Round"
            elif s == 5:
                return "Round"

    def Margin(self, s: int):
        """Semantic interpretation of `margin` value as string."""
        if s == 0:
            return "NA"
        else:
            assert s in range(1, 6), "Margin score out of bounds."
            if s == 1:
                return "Poorly Defined"
            elif s == 2:
                return "Near Poorly Defined"
            elif s == 3:
                return "Medium Margin"
            elif s == 4:
                return "Near Sharp"
            elif s == 5:
                return "Sharp"

    def Lobulation(self, s: int):
        """Semantic interpretation of `lobulation` value as string."""
        if s == 0:
            return "NA"
        else:
            assert s in range(1, 6), "Lobulation score out of bounds."
            if s == 1:
                return "No Lobulation"
            elif s == 2:
                return "Nearly No Lobulation"
            elif s == 3:
                return "Medium Lobulation"
            elif s == 4:
                return "Near Marked Lobulation"
            elif s == 5:
                return "Marked Lobulation"

    def Spiculation(self, s: int):
        """Semantic interpretation of `spiculation` value as string."""
        if s == 0:
            return "NA"
        else:
            assert s in range(1, 6), "Spiculation score out of bounds."
            if s == 1:
                return "No Spiculation"
            elif s == 2:
                return "Nearly No Spiculation"
            elif s == 3:
                return "Medium Spiculation"
            elif s == 4:
                return "Near Marked Spiculation"
            elif s == 5:
                return "Marked Spiculation"

    def Texture(self, s: int):
        """Semantic interpretation of `texture` value as string."""
        if s == 0:
            return "NA"
        else:
            assert s in range(1, 6), "Texture score out of bounds."
            if s == 1:
                return "Non-Solid/GGO"
            elif s == 2:
                return "Non-Solid/Mixed"
            elif s == 3:
                return "Part Solid/Mixed"
            elif s == 4:
                return "Solid/Mixed"
            elif s == 5:
                return "Solid"

    def Malignancy(self, s: int):
        """Semantic interpretation of `malignancy` value as string."""
        if s == 0:
            return "NA"
        else:
            assert s in range(1, 6), "Malignancy score out of bounds."
            if s == 1:
                return "Highly Unlikely"
            elif s == 2:
                return "Moderately Unlikely"
            elif s == 3:
                return "Indeterminate"
            elif s == 4:
                return "Moderately Suspicious"
            elif s == 5:
                return "Highly Suspicious"
