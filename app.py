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
from streamlit.logger import get_logger
import os
from copy import deepcopy
import pandas as pd
import time
import http.client
import json
import matplotlib.font_manager as font_manager
from matplotlib import rcParams
from scipy.interpolate import pchip_interpolate
import datetime
import matplotlib.pyplot as plt
import matplotlib.image as img
import matplotlib.patheffects as path_effects
import matplotlib
import threading
import numpy as np
from PIL import Image
from os import listdir
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import math
path=r'C:\Users\ferna\OneDrive\Escritorio\report'
PATH = path.replace('\\','/')

LOGGER = get_logger(__name__)
dic_status = {
     'Extra Time':'Tiempo Extra',
    'Match Finished':'Finalizado', 
    'Second Half':'2T',
    'Halftime':'Entretiempo',
    'First Half':'1T',
    }

coverage_statistics = [ 61, 144,  71,  39,  78, 135,  88,  94, 140, 179,  62,   2, 203,204, 197,  79,  80, 529,  81, 188, 219, 218, 119, 271,  40,  46,48,  41,  42, 253, 268, 270, 551, 244, 526, 242, 116,  98, 389,
       528,  72,   3, 128, 531,  16,  17, 141, 136, 103,  89,  95, 113,169, 137, 207, 210, 235, 239,  73, 236, 114, 262, 281, 283, 286,288, 292, 307,  10, 106, 172,   5, 265, 323, 332, 345, 373,  31,34,  29,  30, 533,  11,  13, 475, 848]



f_left = '"""\n'
f_rigth = '\n"""'


texto1= ' NanoTeam nace con el propósito de mejorar el **rendimiento** de tus apuestas deportivas de fútbol. \n '
texto2 = ' En nanoteam podrás encontrar todos los resultados de la Premier League y la Primera División de Chile.'
texto3 = ' - Siguenos en Instagram [@nanoteamcl](https://instagram.com/@nanoteamcl).'
z0 = f_left+ texto1+texto2+f_rigth

z =    f"""
        {texto1}
       {texto2}
       {texto3}
         """


import os

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "903a0d7149864011a7b81adaa2c060d9"
    }



def run():
    st.write("# Bienvenido a NanoTeam! 👋⚽")
    st.sidebar.success("Elige alguna categoria.")
    st.markdown( z)

    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    conn.request("GET", "/fixtures?live=all", headers=headers)
    res = conn.getresponse()
    data = res.read()    
    zz = deepcopy(json.loads(data)) 
    response_fixtures_live = { '{}-{}'.format(zz['response'][j]['fixture']['timestamp'] , zz['response'][j]['fixture']['id']) : zz['response'][j] for j in range( min(20,len(zz['response']))  )  }
    fixtures_live = st.empty()
    list_zz = {}
    list_img_live = {}
    for key in response_fixtures_live.keys():
        list_zz[key] = st.empty()
        list_img_live[key] = st.empty()

    while True:
            time.sleep(1)

            conn = http.client.HTTPSConnection("v3.football.api-sports.io")
            conn.request("GET", "/fixtures?live=all", headers=headers)
            res = conn.getresponse()
            data = res.read()
            zz = deepcopy(json.loads(data)) 
            response_fixtures_live = { '{}-{}'.format(zz['response'][j]['fixture']['timestamp'] , zz['response'][j]['fixture']['id']) : zz['response'][j] for j in range( min(20,len(zz['response']))  )  }
            time.sleep(1)
            fixtures_live.markdown('# Actualmente hay {} partidos en vivo'.format(len(zz['response'])))
            
            units = 6
            response_fixtures_statistics_live = { '{}-{}'.format(zz['response'][j]['fixture']['timestamp'] , zz['response'][j]['fixture']['id']) : (zz['response'][j]['fixture']['timestamp'] , zz['response'][j]['fixture']['id'] , zz['response'][j]['teams']['home']['id'] , zz['response'][j]['teams']['away']['id'] ) for j in range( min(20,len(zz['response']))  ) if zz['response'][j]['league']['id'] in  coverage_statistics }
            keys = list(response_fixtures_statistics_live.keys())
            PP = math.ceil( len(keys)/units )+1
            KEYS = [keys[i*PP:(i+1)*PP] for i in range(math.ceil( len(keys)/PP  ))]

            zz_statistics = {}
            def threading_statistics_live(jj ):
                response_fixtures_statistics_live_jj = { key : get_statistics_live(response_fixtures_statistics_live[key][0] ,response_fixtures_statistics_live[key][1] ,response_fixtures_statistics_live[key][2] , response_fixtures_statistics_live[key][3]) for key in KEYS[jj] }
                for key in response_fixtures_statistics_live_jj.keys():
                    zz_statistics[key] = deepcopy(response_fixtures_statistics_live_jj[key])

            dicc = {}
            for jj in range(len(KEYS)):
                dicc[jj] = threading.Thread(target = threading_statistics_live, args=( jj ,))
                dicc[jj].start()
            while True:
                time.sleep(0.2)
                if len(zz_statistics) == len(keys):
                    time.sleep(0.2)
                    break
            zz_statistics = {k:zz_statistics[k] for k in zz_statistics.keys() if len(zz_statistics[k][0])>0 }

            dic_stats_type = {'Shots on Goal':'Tiros al arco', 'Shots off Goal':'Tiros fuera', 'Total Shots':'Total de Tiros', 
                   'Shots insidebox':'Tiros dentro del área', 'Shots outsidebox':'Tiros fuera del area', 'Fouls':'Faltas', 'Corner Kicks':'Corners',
                   'Offsides':'Fuera de juego', 'Ball Possession':'Posesión de balón', 'Yellow Cards':'Tarjetas Amarillas', 'Red Cards':'Tarjetas Rojas',
                   'Goalkeeper Saves':'Atajadas','Blocked Shots':'Tiros Tapados',
                   'Total passes':'Total de Pases', 'Passes accurate':'Pases correctos', 'Passes %': '%Pases correctos' }

            def stats_value(x):
                if type(x) == type(None):
                    return 0
                else:
                    return x
            # key = '1666630800-881706'
            statistics_live = {  key : { 'home' :{ 'id':  zz_statistics[key][0][0]['team']['id'], 'name':  zz_statistics[key][0][0]['team']['name']  ,  'statistics' :  { dic_stats_type[zz_statistics[key][0][0]['statistics'][j0]['type']]: stats_value(zz_statistics[key][0][0]['statistics'][j0]['value']) for j0 in range(len( zz_statistics[key][0][0]['statistics']))  }   }  , 'away' :{ 'id':  zz_statistics[key][1][0]['team']['id'] ,'name':  zz_statistics[key][1][0]['team']['name'],  'statistics' : { dic_stats_type[zz_statistics[key][1][0]['statistics'][j0]['type']] : stats_value(zz_statistics[key][1][0]['statistics'][j0]['value']) for j0 in range(len( zz_statistics[key][1][0]['statistics']))  }   } }  for key in  zz_statistics.keys()  }

            st.write((len(statistics_live)))
            for key in list_zz.keys():
                if key not in response_fixtures_live.keys():
                    list_zz[key].empty()
                    list_img_live[key].empty()
            for key in response_fixtures_live.keys():
                if key not in list_zz.keys():
                    list_zz[key] = st.empty()
                    list_img_live[key] = st.empty()

            list_zz = { k: list_zz[k] for k in list_zz.keys() if k in response_fixtures_live.keys()   }
            list_img_live = { k: list_img_live[k] for k in list_img_live.keys() if k in response_fixtures_live.keys()   }
               

            for key in response_fixtures_live.keys():
              fix = response_fixtures_live[key]
              if (str(int(fix['fixture']['status']['elapsed'])) == '45' ) :
                    elapsed = '45'+' extra'
              elif (str(int(fix['fixture']['status']['elapsed'])) == '90' ) :
                    elapsed = '90'+' extra'
              else:
                  elapsed = str(int(fix['fixture']['status']['elapsed']))
              try:  
                body = """
                <center>
                    <details>
                          <summary markdown="span">Click acá para ver las estadisticas TRY</summary>
                          This is the detailed text.
                          We can still use markdown, but we need to take the additional step of using the `parse_block_html` option as described in the [Mix HTML + Markdown Markup section](#mix-html--markdown-markup).
                          You can learn more about expected usage of this approach in the [GitLab UI docs](https://gitlab-org.gitlab.io/gitlab-ui/?path=/story/base-collapse--default) though the solution we use above is specific to usage in markdown.
                    </details>
                <h3 style="color:#174a65">{} vs {} </h3>
                </center>
                """.format(fix['teams']['home']['name'] , fix['teams']['away']['name']   )
                list_zz[key].markdown( body ,unsafe_allow_html=True)
                try :
                     #list_img_live[key].columns([1,5,1])[1].pyplot(  create_image_fix_livescore1(fix , elapsed))
                     list_img_live[key].columns([1,5,4])[1].pyplot(  create_image_statistics_fix_livescore1(key))
                     st.write(key)
                except:
                    #list_img_live[key].columns([1,5,1])[1].pyplot(  create_image_fix_livescore1(fix , elapsed))
                    st.write('no se logro1111')
                    pass
                if key in      statistics_live.keys():
                   list_img_live[key][1].pyplot(  create_image_statistics_fix_livescore1(key))
              except:
                    list_zz[key] = st.empty()
                    list_img_live[key]  = st.empty()
                    body = """
                    <center>
                        <details>
                              <summary markdown="span">Click aca para ver las estadisticas EXCEPT</summary>
                              This is the detailed text.
                              We can still use markdown, but we need to take the additional step of using the 'parse_block_html' option as described in the [Mix HTML + Markdown Markup section](#mix-html--markdown-markup).
                              You can learn more about expected usage of this approach in the [GitLab UI docs](https://gitlab-org.gitlab.io/gitlab-ui/?path=/story/base-collapse--default) though the solution we use above is specific to usage in markdown.
                        </details>
                    <h3 style="color:#174a65">{} vs {} </h3>
                    </center>
                    """.format(fix['teams']['home']['name'] , fix['teams']['away']['name']   )
                    list_zz[key].markdown( body ,unsafe_allow_html=True)
                    #image = Image.open( r'C:\Users\ferna\OneDrive\Escritorio\report\football\nanoteamcl\img_fixtures_live\{}_0.png'.format(fix['fixture']['id'])  )
                    st.write('no se logro')
                    #list_img_live[key].columns([1,5,1])[1].pyplot(  create_image_fix_livescore1(fix , elapsed))

if __name__ == "__main__":
        st.set_page_config(
        page_title="NT ⚽🔮",
        page_icon="👋",
        layout="wide"
        )
        run()
