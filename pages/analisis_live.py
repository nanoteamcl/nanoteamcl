# Copyright 2018-2022 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import inspect
import textwrap
import pandas as pd
import altair as alt
from streamlit.hello.utils import show_code

from urllib.error import URLError

import plotly.express as px
# import sys
# sys.modules[__name__].__dict__.clear()
import os
path=r'C:\Users\ferna\OneDrive\Escritorio\report'
os.chdir(path+'\\football')
PATH = path.replace('\\','/')
import pandas as pd
import http.client
from copy import deepcopy

import datetime
from datetime import timedelta

df = pd.read_csv( path+'\\football\\FIXTURES_full.csv' ,low_memory =False )
def indexx(x):
    x.index = range(len(x))
    return x
def normalize_df_fixture(df):
    df['team_id'] = [str(int(x)) for x in df['team_id'] ]
    df['team_rival_id'] = [str(int(x)) for x in df['team_rival_id'] ]
    df['team_home_id'] = [str(int(x)) for x in df['team_home_id'] ]
    df['team_away_id'] = [str(int(x)) for x in df['team_away_id'] ]
    df['season'] = [str(int(x)) for x in df['season'] ]
    df['fixture_id'] = [str(int(x)) for x in df['fixture_id']]
    df['league_id'] = [str(int(x)) for x in df['league_id']]
    df['timestamp'] = deepcopy(  pd.to_datetime(df.date) )
    df['timestamp'] =[  d-timedelta(hours = 3) for d in df.timestamp ]
    df['timestamp'] = df['timestamp'].dt.tz_localize(None)
    df['date'] =[  str(d.date()) for d in df.timestamp ]
    df['fix-team'] = [ df.loc[i,'fixture_id'] + '-'+  df.loc[i,'team_id'] for i in df.index]
    return df

df = normalize_df_fixture(df)
df_full = deepcopy(df)
df_full_c = df_full[df_full.country == 'Chile']
count1 = pd.to_datetime(datetime.datetime.now())
count2 = count1+timedelta(hours = 2)

date0 = pd.to_datetime(datetime.datetime.now())
date0_str = str(pd.to_datetime(datetime.datetime.now()).date())
df_day = indexx(df_full[df_full['timestamp']>= datetime.datetime.now()])


import streamlit as st
from streamlit.logger import get_logger
import os
import pandas as pd



st.set_page_config(page_title="DataFrame Demo", page_icon="📊")
st.markdown("# DataFrame Demo")
st.sidebar.header("DataFrame Demo")
st.write(
    """This demo shows how to use `st.write` to visualize Pandas DataFrames.
(Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
)

body = """
<center>
<details>
<summary markdown="span">This is the summary text, click me to expand</summary>

This is the detailed text.{} vs {}

We can still use markdown, but we need to take the additional step of using the `parse_block_html` option as described in the [Mix HTML + Markdown Markup section](#mix-html--markdown-markup).

You can learn more about expected usage of this approach in the [GitLab UI docs](https://gitlab-org.gitlab.io/gitlab-ui/?path=/story/base-collapse--default) though the solution we use above is specific to usage in markdown.
</details>
<h1 style="color:blue">some *This is Blue italic.* text</h1>

</center>
""".format(df_day.loc[0,'team_home_name'] , df_day.loc[0,'team_away_name'])
st.markdown( body , unsafe_allow_html=True)


show_code(data_frame_demo)
