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
# Modified   : Sunday July 31st 2022 09:03:52 pm                                                   #
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
