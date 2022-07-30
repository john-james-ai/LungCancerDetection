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
# Modified   : Friday July 29th 2022 08:44:58 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : BSD 3-clause "New" or "Revised" License                                             #
# Copyright  : (c) 2022 John James                                                                 #
# ================================================================================================ #
import pandas as pd

# ------------------------------------------------------------------------------------------------ #
annotation_columns = [
    "patient_id",
    "nodule_no",
    "annotation_no",
    "subtlety",
    "internalStructure",
    "calcification",
    "sphericity",
    "margin",
    "lobulation",
    "spiculation",
    "texture",
    "malignancy",
    "diameter",
    "volume",
    "surface_area",
]
annotation_kind = [
    "id",
    "id",
    "id",
    "characteristic",
    "characteristic",
    "characteristic",
    "characteristic",
    "characteristic",
    "characteristic",
    "characteristic",
    "characteristic",
    "characteristic",
    "size",
    "size",
    "size",
]

annotation_types = [
    "nominal",
    "nominal",
    "nominal",
    "ordinal",
    "nominal",
    "nominal",
    "nominal",
    "ordinal",
    "ordinal",
    "ordinal",
    "nominal",
    "ordinal",
    "metric",
    "metric",
    "metric",
]
a = {
    "column": annotation_columns,
    "kind": annotation_kind,
    "type": annotation_types,
}
ANNOTATION_COLUMNS = pd.DataFrame.from_dict(a, orient="columns")

# ------------------------------------------------------------------------------------------------ #
nodule_columns = annotation_columns
nodule_kind = annotation_kind
nodule_types = annotation_types
nodule_columns.append("n_annotations")
nodule_kind.append("annotation")
nodule_types.append("count")
n = {
    "column": nodule_columns,
    "kind": nodule_kind,
    "type": nodule_types,
}
NODULE_COLUMNS = pd.DataFrame.from_dict(n, orient="columns")
