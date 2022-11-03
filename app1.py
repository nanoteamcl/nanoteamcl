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
    'Penalty in progress' :'Penal en progreso'
    }

os.chdir(path+'\\football\\nanoteamcl')
def get_statistics_live(timestamp , fixture_id , team_home_id , team_away_id):
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    conn.request("GET", "/fixtures/statistics?fixture={}&team={}".format(fixture_id , team_home_id), headers = headers)
    res = conn.getresponse()
    zz_home = deepcopy(json.loads(res.read()))

    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    conn.request("GET", "/fixtures/statistics?fixture={}&team={}".format(fixture_id , team_away_id), headers = headers)
    res = conn.getresponse()
    zz_away = deepcopy(json.loads(res.read()))
    return [zz_home['response'] , zz_away['response']]


def create_image_statistics_fix_livescore1(statistics_live,key):
    fontname = font_manager.FontProperties(fname=r"C:\Users\ferna\Downloads\Roboto\Roboto-Bold.ttf")
    x = np.linspace(5,25,100)
    y = [ 0.5*f-1 for f in x]
    my_dpi = 200

    fig, ax = plt.subplots( figsize=(3,3), dpi=200)
    plt.plot(x, y, color = 'white')
    x_stats_name = 15
    x_stats_home = 22
    x_stats_separate = 5
    x_medium = x_stats_home+x_stats_separate
    x_stats_away = x_medium+(x_medium-x_stats_home)
    y_space  = 0.9
    
    zoom = 0.4
    team_home_id = str(int( statistics_live[key]['home']['id']  ))
    team_away_id = str(int(  statistics_live[key]['away']['id'] ))
    y_inicio = 9
    ll = -2
    plt.text(  x_stats_home , y_inicio-y_space*ll,'Local' ,ha = 'center',fontsize = 9)      
    plt.text(  x_stats_away ,y_inicio -y_space*ll , 'Visita' ,ha = 'center',fontsize = 9)      
    type_statistics = ['Tiros al arco', 
                               'Tiros dentro del área',
                               'Corners',
                               'Posesión de balón',
                               'Tarjetas Amarillas',
                               'Tarjetas Rojas',
                               '%Pases correctos',
                               'Total de Pases'      ]
    for ll in range(len(type_statistics)):
        plt.text(  x_stats_name ,y_inicio -y_space*ll , type_statistics[ll] , ha = 'right' ,fontsize = 10)      
        plt.text(  x_stats_home ,y_inicio -y_space*ll,'{}'.format( statistics_live[key]['home']['statistics'][ type_statistics[ll] ]) ,ha = 'center',fontsize = 10)      
        plt.text(  x_stats_away , y_inicio-y_space*ll , '{}'.format( statistics_live[key]['away']['statistics'][ type_statistics[ll] ]) ,ha = 'center',fontsize = 10)      

    plt.axis('off')
    plt.xticks([])
    plt.yticks([])
    # plt.show()
    # fig.savefig(   r'C:\Users\ferna\OneDrive\Escritorio\report\football\nanoteamcl\img_fixtures_live\{}_00.png'.format(key)  ,dpi = my_dpi,bbox_inches='tight') 

    matplotlib.pyplot.close(fig)
    return fig
    



def create_image_fix_livescore1(fix , elapsed):
    fontname = font_manager.FontProperties(fname=r"C:\Users\ferna\Downloads\Roboto\Roboto-Bold.ttf")
    x = np.linspace(-10,50,100)
    y = [ 0.2*f for f in x]
    my_dpi = 400

    fig, ax = plt.subplots( figsize=(8,1.5), dpi=200)
    #fig.set_size_inches(8, 1.5)
    plt.plot(x, y, color = 'white')
    x_goal_home = 15
    x_goal_separate = 5
    x_medium = x_goal_home+x_goal_separate
    x_goal_away = x_medium+(x_medium-x_goal_home)
    y_goals = 3
    zoom = 0.4
    x_shield_home = 5
    x_shield_separate = 10
    x_shield_away = x_medium+(x_medium-x_shield_home)
    y_shield = 4
    y_status_short = 0
    
    
    x_time = 40
    y_time = 10

    team_home_id = str(int( fix['teams']['home']['id']  ))
    team_away_id = str(int( fix['teams']['away']['id']  ))
    try:
        image_name_home = 'team_{}_logo.png'.format(team_home_id)
        image_home = plt.imread(path + '\\football\\media_teams\\'+image_name_home)
        image_name_away = 'team_{}_logo.png'.format(team_away_id)
        image_away = plt.imread(path + '\\football\\media_teams\\'+image_name_away)

        imagebox_home = OffsetImage(image_home, zoom = zoom) # tamaño imagen
        xy_home = [ x_shield_home , y_shield ] # Coordenadas del centro de la imagen
        ab_image_home = AnnotationBbox(imagebox_home, xy_home, xybox=(0, 0), boxcoords='offset points', bboxprops = dict(visible = False))
        ax.add_artist(ab_image_home)
        imagebox_away = OffsetImage(image_away, zoom = zoom) # tamaño imagen
        xy_away = [ x_shield_away,y_shield ] # Coordenadas del centro de la imagen
        ab_image_away = AnnotationBbox(imagebox_away, xy_away, xybox=(0, 0), boxcoords='offset points', bboxprops = dict(visible = False))
        ax.add_artist(ab_image_away)


    except:
        image = plt.imread(path + '\\football\\media_teams\\image_not_available.png')
        imagebox = OffsetImage(image, zoom = zoom) # tamaño imagen
        xy = [ x_shield_home,y_shield ] # Coordenadas del centro de la imagen
        ab_image = AnnotationBbox(imagebox, xy, xybox=(0, 0), boxcoords='offset points', bboxprops = dict(visible = False))
        ax.add_artist(ab_image)
        image = plt.imread(path + '\\football\\media_teams\\image_not_available.png')
        imagebox = OffsetImage(image, zoom = zoom) # tamaño imagen
        xy = [ x_shield_away,y_shield ] # Coordenadas del centro de la imagen
        ab_image = AnnotationBbox(imagebox, xy, xybox=(0, 0), boxcoords='offset points', bboxprops = dict(visible = False))
        ax.add_artist(ab_image)
 
    

    plt.text( x_goal_home , y_goals , str(int(fix['goals']['home']))  ,fontsize = 30,ha = 'center',color = '#174a65', fontproperties=fontname,path_effects=[path_effects.withSimplePatchShadow(offset=(0.1, - 0.05))])       
    plt.text( x_medium , y_goals , '-'   ,fontsize = 30 ,ha = 'center',color = '#174a65', fontproperties=fontname,path_effects=[path_effects.withSimplePatchShadow(offset=(0.1, - 0.1))])       
    plt.text( x_goal_away , y_goals , str(int(fix['goals']['away']))   ,fontsize = 30 , ha = 'center',color = '#174a65', fontproperties=fontname,path_effects=[path_effects.withSimplePatchShadow(offset=(0.1, - 0.1))])       
    if  fix['fixture']['status']['long']!= 'Halftime':
       plt.text( x_time , y_time , dic_status[fix['fixture']['status']['long']] +' ' + elapsed+ '° EN VIVO'  ,fontsize = 10,ha = 'center',color = '#64b252', fontproperties=fontname,
              path_effects=[path_effects.withSimplePatchShadow(offset=(0.3, - 0.3)) ,  path_effects.Normal(), path_effects.Stroke(linewidth=0.2, foreground='black')])
    else:
        plt.text( x_time , y_time , dic_status[fix['fixture']['status']['long']] ,fontsize = 10,ha = 'center',color = '#64b252', fontproperties=fontname,
               path_effects=[path_effects.withSimplePatchShadow(offset=(0.3, - 0.3)) ,  path_effects.Normal(), path_effects.Stroke(linewidth=0.2, foreground='black')])
    
    
    #if fix['league']['id'] in coverage_statistics:
    #    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    #    conn.request("GET", "/fixtures/events?fixture=".format(967823), headers=headers)
    #    res = conn.getresponse()
    #    data_events = json.loads(res.read()):
    kk0 = 0
    
    x_events_home = 10
    x_events_away = 20
    y_events = 20
    y_events_delta = 1
    events1 = [ x for x in fix['events'] if  x['type'] == 'Goal'  ]
    if len( events1  )>0:
        for l0 in range(len(  events1 )):
            if events1[l0]['team']['id'] ==  fix['teams']['home']['id']:
                plt.text( x_events_home , y_events -l0*y_events_delta , '{} {}'.format(events1[l0]['detail'] , str(events1[l0]['time']['elapsed']))  ,fontsize = 10,ha = 'center',color = '#64b252', fontproperties=fontname,
                       path_effects=[path_effects.withSimplePatchShadow(offset=(0.3, - 0.3)) ,  path_effects.Normal(), path_effects.Stroke(linewidth=0.2, foreground='black')])
            else:
                plt.text( x_events_away , y_events -l0*y_events_delta , events1[l0]['detail'] +' ' +str(events1[l0]['time']['elapsed'])    ,fontsize = 10,ha = 'center',color = '#64b252', fontproperties=fontname,
                       path_effects=[path_effects.withSimplePatchShadow(offset=(0.3, - 0.3)) ,  path_effects.Normal(), path_effects.Stroke(linewidth=0.2, foreground='black')])
                


    plt.axis('off')
    plt.xticks([])
    plt.yticks([])
    matplotlib.pyplot.close(fig)
    return fig
coverage_statistics = [ 61, 144,  71,  39,  78, 135,  88,  94, 140, 179,  62,   2, 203,204, 197,  79,  80, 529,  81, 188, 219, 218, 119, 271,  40,  46,48,  41,  42, 253, 268, 270, 551, 244, 526, 242, 116,  98, 389,
       528,  72,   3, 128, 531,  16,  17, 141, 136, 103,  89,  95, 113,169, 137, 207, 210, 235, 239,  73, 236, 114, 262, 281, 283, 286,288, 292, 307,  10, 106, 172,   5, 265, 323, 332, 345, 373,  31,34,  29,  30, 533,  11,  13, 475, 848]


# coverage_statistics = [2]  

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
    response_fixtures_live = { '{}-{}'.format(zz['response'][j]['fixture']['timestamp'] , zz['response'][j]['fixture']['id']) : zz['response'][j] for j in range( min(100,len(zz['response']))  ) }
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
            response_fixtures_live = { '{}-{}'.format(zz['response'][j]['fixture']['timestamp'] , zz['response'][j]['fixture']['id']) : zz['response'][j] for j in range( min(100,len(zz['response']))  )  }
            time.sleep(1)
            
            units = 6
            response_fixtures_statistics_live = { '{}-{}'.format(zz['response'][j]['fixture']['timestamp'] , zz['response'][j]['fixture']['id']) : (zz['response'][j]['fixture']['timestamp'] , zz['response'][j]['fixture']['id'] , zz['response'][j]['teams']['home']['id'] , zz['response'][j]['teams']['away']['id'] ) for j in range( min(100,len(zz['response']))  ) if  zz['response'][j]['league']['id'] in coverage_statistics }
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
                time.sleep(0.1)
                if len(zz_statistics) == len(keys):
                    time.sleep(0.1)
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
            fixtures_live.markdown('# Actualmente hay {} partidos en vivo y {} partidos con estadísticas'.format(len(zz['response']) , len(statistics_live)))

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
               # st.write(statistics_live)
               fix = response_fixtures_live[key]
               try:
                   if (str(int(fix['fixture']['status']['elapsed'])) == '45' ) :
                         elapsed = '45\''+' extra'
                   elif (str(int(fix['fixture']['status']['elapsed'])) == '90' ) :
                         elapsed = '90\''+' extra'
                   else:
                       elapsed = str(int(fix['fixture']['status']['elapsed']))
               except:
                   elapsed = '\''
               try:  
                body = """
                <center>
                    <details>
                          <summary markdown="span">Click acá para ver las estadisticas TRY</summary>
                          This is the detailed text.
                          We can still use markdown, but we need to take the additional step of using the option as described in the [Mix HTML + Markdown Markup section](#mix-html--markdown-markup).
                          You can learn more about expected usage of this approach in the [GitLab UI docs](https://gitlab-org.gitlab.io/gitlab-ui/?path=/story/base-collapse--default) though the solution we use above is specific to usage in markdown.
                    </details>
                <h3 style="color:#174a65">{} {} vs {} {} ---{}</h3>
                </center>
                """.format(fix['teams']['home']['name'] ,fix['teams']['home']['id'], fix['teams']['away']['name'] , fix['teams']['away']['id']  , fix['fixture']['id']  )
                list_zz[key].markdown( body ,unsafe_allow_html=True)
                list_img_live[key].columns([1,5,3])[1].pyplot( create_image_fix_livescore1(fix , elapsed))
                try:
                   list_img_live[key].columns([1,5,3])[2].pyplot(   create_image_statistics_fix_livescore1( statistics_live , key))
                except:
                    pass
               except:
                    list_zz[key] = st.empty()
                    list_img_live[key]  = st.empty()
                    body = """
                    <center>
                        <details>
                              <summary markdown="span">Click aca para ver las estadisticas EXCEPT</summary>
                              This is the detailed text.
                              We can staill use markdown, but we need to take the additional step of using the  option as described in the [Mix HTML + Markdown Markup section](#mix-html--markdown-markup).
                              You can learn more about expected usage of this approach in the [GitLab UI docs](https://gitlab-org.gitlab.io/gitlab-ui/?path=/story/base-collapse--default) though the solution we use above is specific to usage in markdown.
                        </details>
                    <h3 style="color:#174a65">{} vs {} </h3>
                    </center>
                    """.format(fix['teams']['home']['name'] , fix['teams']['away']['name']   )
                    list_zz[key].markdown( body ,unsafe_allow_html=True)
                    st.write('no se logro')
                    list_img_live[key].columns([1,5,3])[1].pyplot(  create_image_fix_livescore1(fix , elapsed))
                    try:
                       list_img_live[key].columns([1,5,3])[2].pyplot(   create_image_statistics_fix_livescore1( statistics_live , key))
                    except:
                        pass


if __name__ == "__main__":
        st.set_page_config(
        page_title="NT ⚽🔮",
        page_icon="👋",
        layout="wide"
        )
        run()
