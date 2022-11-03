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
import numpy as np
import base64
from PIL import Image
svg = './standings/standings_Premier League1.svg'

def show_table_premier_league():
    image = Image.open('./standings/standings_Premier League1.png')
    st.image(image, caption ='Standings Premier League')
   

st.set_page_config(page_title="Premier League", page_icon="📊")
st.markdown("# Premier League")
st.markdown("## Standings")

st.sidebar.header("Premier League")
st.write(
    """ En esta sección analizamos los partidos de la semana de la Premier League, siguenos en instragram [@nanoteamcl](http://instagram.com/nanoteamcl).)"""
)
show_table_premier_league()

#show_code(show_table_premier_league)
