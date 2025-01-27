#  Copyright 2019-2020 The Lux Authors.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

#  SPDX-FileCopyrightText: Copyright (c) 2022, NVIDIA CORPORATION & AFFILIATES. All rights reserved.

import pandas as pd
from global_backend import backend
#If the backend is set to holoviews, then override cudf not pandas
if backend.set_back =="holoviews":
    import cudf
    overrideCudf=True
else:
    overrideCudf=False
    
from .frame import LuxDataFrame
from .groupby import LuxDataFrameGroupBy, LuxSeriesGroupBy
from .series import LuxSeries

global originalDF
# Keep variable scope of original pandas df
originalDF = pd.core.frame.DataFrame if backend.set_back !="holoviews" else cudf.core.dataframe.DataFrame
originalSeries = pd.core.series.Series if backend.set_back !="holoviews" else cudf.core.series.Series 

def setOption(overridePandas=True,overrideCudf=False):
    if overrideCudf:
        cudf.DataFrame = cudf.core.dataframe.DataFrame = LuxDataFrame
        cudf.Series = cudf.core.series.Series  = LuxSeries
        cudf.core.groupby.groupby.DataFrameGroupBy = LuxDataFrameGroupBy
        cudf.core.groupby.groupby.SeriesGroupBy = LuxSeriesGroupBy
    elif overridePandas:
        pd.DataFrame = (
            pd.io.json._json.DataFrame
        ) = (
            pd.io.sql.DataFrame
        ) = (
            pd.io.excel.DataFrame
        ) = (
            pd.io.formats.DataFrame
        ) = (
            pd.io.sas.DataFrame
        ) = (
            pd.io.clipboards.DataFrame
        ) = (
            pd.io.common.DataFrame
        ) = (
            pd.io.feather_format.DataFrame
        ) = (
            pd.io.gbq.DataFrame
        ) = (
            pd.io.html.DataFrame
        ) = (
            pd.io.orc.DataFrame
        ) = (
            pd.io.parquet.DataFrame
        ) = (
            pd.io.pickle.DataFrame
        ) = (
            pd.io.pytables.DataFrame
        ) = (
            pd.io.spss.DataFrame
        ) = (
            pd.io.stata.DataFrame
        ) = pd.io.api.DataFrame = pd.core.frame.DataFrame = pd._testing.DataFrame = LuxDataFrame
        if pd.__version__ < "1.3.0":
            pd.io.parsers.DataFrame = LuxDataFrame
        else:
            pd.io.parsers.readers.DataFrame = LuxDataFrame
        pd.Series = pd.core.series.Series = pd.core.groupby.ops.Series = pd._testing.Series = LuxSeries
        pd.core.groupby.generic.DataFrameGroupBy = LuxDataFrameGroupBy
        pd.core.groupby.generic.SeriesGroupBy = LuxSeriesGroupBy
    else:
        pd.DataFrame = pd.io.parsers.DataFrame = pd.core.frame.DataFrame = originalDF
        pd.Series = originalSeries

overridePandas=True
setOption(overridePandas, overrideCudf)
