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
from PIL import Image

league_name = 'Primera División'

png = './standings/standings_Primera División1.png'

def show_table_premier_league():
    image = Image.open(png)
    st.image(image, caption ='Standings '+league_name)
   

st.set_page_config(page_title=league_name, page_icon="📊")
st.markdown("# "+league_name)
st.markdown("## "+league_name)

st.sidebar.header(league_name)
st.write(
    " En esta sección analizamos los partidos de la semana de la "+league_name+", siguenos en instragram [@nanoteamcl](http://instagram.com/nanoteamcl).)"
)
show_table_premier_league()

#show_code(show_table_premier_league)
