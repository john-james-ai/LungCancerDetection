#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Lung Cancer Detection                                                               #
# Version    : 0.1.0                                                                               #
# Filename   : /analysis.py                                                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/LungCancerDetection                                #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday July 27th 2022 03:49:40 pm                                                #
# Modified   : Sunday July 31st 2022 04:55:18 am                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : BSD 3-clause "New" or "Revised" License                                             #
# Copyright  : (c) 2022 John James                                                                 #
# ================================================================================================ #
import os
import pandas as pd
import numpy as np
import logging
import logging.config
import seaborn as sns
import matplotlib.pyplot as plt

from lcd.utils.config import DataConfig

# ------------------------------------------------------------------------------------------------ #
logging.config.fileConfig(fname="config/log.conf")
logger = logging.getLogger(__name__)
sns.set_palette("Blues_d")
sns.set_style("whitegrid")
# ------------------------------------------------------------------------------------------------ #


class LIDCExplorer:
    """Class provides methods for graphical and non-graphical exploratory data analysis."""

    def __init__(self) -> None:

        self._annotation_filepath = os.path.join(DataConfig().raw_data_folder, "annotations.csv")
        self._nodule_filepath = os.path.join(DataConfig().raw_data_folder, "nodules.csv")

        self._annotation_data = None
        self._nodule_data = None

        self._load()

    def nodule_summary(self) -> pd.DataFrame:
        """Produces a 4x3 DataFrame of nodule counts by at least 1,2,3,4 readers"""
        n_readers = self._nodule_data["n_readers"].max()
        n_nodules = self._nodule_data.shape[0]
        summary_data = np.zeros((n_readers, 3))
        for i in range(n_readers):
            summary_data[i, 0] = i + 1
            summary_data[i, 1] = int(self._nodule_data[self._nodule_data["n_readers"] > i].shape[0])
            summary_data[i, 2] = round(summary_data[i, 1] / n_nodules, 2)
        df = pd.DataFrame(summary_data, columns=["At Least N Readers", "Nodules", "Ratio"])
        return df

    def nodules_by_biomarker(self) -> pd.DataFrame:
        """Produces a matrix of nodule counts by biomarker levels"""
        biomarkers = [
            "subtlety",
            "internalStructure",
            "calcification",
            "sphericity",
            "margin",
            "lobulation",
            "spiculation",
            "texture",
        ]
        levels = range(1, 7)
        for biomarker, level in zip(biomarkers, levels):
            self._nodule_data[biomarker].groupby(biomarker).count()

    def malignancy_summary(self) -> pd.DataFrame:
        """Provides malignancy data for nodules by at least 1,2,3,4 readers

        Args:
            normalize (bool): If True, the counts are normalized to values in [0,1]

        """
        n_readers = self._nodule_data["n_readers"].max()
        n_malignancy_values = self._nodule_data["malignancy"].max()

        summary_data = np.zeros((n_readers, n_malignancy_values + 1))
        for i in range(n_readers):
            for j in range(1, n_malignancy_values + 1):  # +1 For n_readers column
                summary_data[i, 0] = i + 1
                summary_data[i, j] = len(
                    self._nodule_data[
                        (self._nodule_data["n_readers"] > i)
                        & (self._nodule_data["malignancy"] == j)
                    ]["nodule_id"]
                )

        df = pd.DataFrame(
            summary_data,
            columns=[
                "At Least N Readers",
                "Highly Unlikely ",
                "Moderately Unlikely",
                "Indeterminate",
                "Moderately Suspicious",
                "Highly Suspicious",
            ],
        )
        return df

    def diameter_stats(self) -> pd.DataFrame:
        """Provides descriptive statistics of nodule diameter estimates."""
        return self._annotation_data["diameter"].describe().to_frame().T

    def diameter_stats_by_malignancy(self) -> pd.DataFrame:
        """Provides descriptive statistics of nodule diameter estimates by malignancy."""
        return self._annotation_data[["malignancy", "diameter"]].groupby("malignancy").describe().T

    def diameter_stats_by_diagnosis(self) -> pd.DataFrame:
        """Provides descriptive statistics of nodule diameter estimates by diagnosis."""
        return self._annotation_data[["diagnosis", "diameter"]].groupby("diagnosis").describe().T

    def diameter_plot_by_malignancy(self) -> None:
        fig, axes = plt.subplots(figsize=(12, 8))
        axes = sns.boxplot(
            x=self._annotation_data["malignancy"], y=self._annotation_data["diameter"]
        )
        axes.set_title("Nodule Diameter by Malignancy")
        plt.show()

    def diameter_plot_by_diagnosis(self) -> None:
        fig, axes = plt.subplots(figsize=(12, 8))
        axes = sns.boxplot(
            x=self._annotation_data["diagnosis"], y=self._annotation_data["diameter"]
        )
        axes.set_title("Nodule Diameter by Diagnosis")
        plt.show()

    def _load(self) -> None:
        self._annotation_data = self._read(self._annotation_filepath)
        self._nodule_data = self._read(self._nodule_filepath)

    def _read(self, filepath: str) -> pd.DataFrame:
        """Loads existing metadata if it exists."""
        try:
            return pd.read_csv(filepath, engine="pyarrow")
        except FileNotFoundError as e:
            logger.error("File {} not found.\n{}".format(filepath, e))
            raise
