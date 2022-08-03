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
# Modified   : Monday August 1st 2022 03:54:38 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : BSD 3-clause "New" or "Revised" License                                             #
# Copyright  : (c) 2022 John James                                                                 #
# ================================================================================================ #

ANNOTATION_COLUMNS = [
    "patient_id",
    "scan_id",
    "nodule_classification",
    "nodule_id",
    "annotation_no",
    "annotation_id",
    "n_readers",
    "subtlety",
    "internalStructure",
    "calcification",
    "sphericity",
    "margin",
    "lobulation",
    "spiculation",
    "texture",
    "malignancy",
    "Subtlety",
    "InternalStructure",
    "Calcification",
    "Sphericity",
    "Margin",
    "Lobulation",
    "Spiculation",
    "Texture",
    "Malignancy",
    "diameter",
    "volume",
    "surface_area",
    "diagnosis",
    "slice_thickness",
    "slice_spacing",
    "pixel_spacing",
]

NODULE_COLUMNS = [
    "patient_id",
    "scan_id",
    "nodule_classification",
    "nodule_id",
    "annotation_no",
    "annotation_id",
    "n_readers",
    "subtlety",
    "internalStructure",
    "calcification",
    "sphericity",
    "margin",
    "lobulation",
    "spiculation",
    "texture",
    "malignancy",
    "Subtlety",
    "InternalStructure",
    "Calcification",
    "Sphericity",
    "Margin",
    "Lobulation",
    "Spiculation",
    "Texture",
    "Malignancy",
    "diameter",
    "volume",
    "surface_area",
    "diagnosis",
]

SMALL_NODULE_COLUMNS = [
    "patient_id",
    "scan_id",
    "nodule_classification",
    "nodule_id",
    "malignancy",
    "Malignancy",
    "diameter",
    "diagnosis",
]


FEATURE_COLUMNS = [
    "subtlety",
    "internalStructure",
    "calcification",
    "sphericity",
    "margin",
    "lobulation",
    "spiculation",
    "texture",
    "malignancy",
]

SEMANTIC_FEATURE_COLUMNS = [
    "Subtlety",
    "InternalStructure",
    "Calcification",
    "Sphericity",
    "Margin",
    "Lobulation",
    "Spiculation",
    "Texture",
    "Malignancy",
]

CASE_COLUMNS = [
    "patient_id",
    "total_nodules",
    "n_nodules_lt_3mm",
    "n_nodules_ge_3mm",
    "n_non_nodules_ge_3mm",
    "n_nodules_benign",
    "n_nodules_malignant",
    "filepath",
    "n_images",
    "total_file_size",
]
