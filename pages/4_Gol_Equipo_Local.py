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

cols_1 = [ 'home_p_mas_15', 'away_p_mas_15',  'season',  'country', 'name_league','match']
def show_data_today():
    try:
        df = pd.read_excel('data1.xlsx')
        df.index = df['match']
        df = df[cols_1]
        matchs = st.multiselect(
            "Seleccione los partidos que desea", list(df.match)[0:1000], list(df.match)[0:150000]
        )
        if not matchs:
            st.error("Por favor seleccione un partido.")
        else:    
                df_sel = df[df.match.isin(  list(matchs) )]
                st.dataframe(df_sel,1000,50*len(matchs))


                df_styled = df_sel[[  'home_p_mas_15', 'away_p_mas_15' ]].style.format(formatter="{:.1f}", na_rep=".").bar(cmap="Greens")
                st.header("Styling is there with st.table")
                st.write("Code: st.table(data=df_styled)")
                st.table(data=df_styled)





    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**
            Connection error: %s
        """
            % e.reason
        )


st.set_page_config(page_title=" Analisis today1", page_icon="📊")
st.markdown("# Analisis today2")
st.sidebar.header("Analisis today3")
st.write(
    """ Aca mostramos los partidos del dia, siguenos en instragram [@nanoteamcl](http://instagram.com/nanoteamcl).)"""
)

show_data_today()

show_code(show_data_today)
