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


def create_image_statistics_fix_livescore1(key):
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
        image_name_home = [x for x in listdir(path + '\\football\\media_teams') if team_home_id+'_' == x[0:len(team_home_id)+1]] [0]
        image_home = plt.imread(path + '\\football\\media_teams\\'+image_name_home)
        image_name_away = [x for x in listdir(path + '\\football\\media_teams') if team_away_id+'_' == x[0:len(team_away_id)+1]] [0]
        image_away = plt.imread(path + '\\football\\media_teams\\'+image_name_away)

        imagebox_home = OffsetImage(image_home, zoom = zoom) # tamaño imagen
        xy_home = [ x_shield_home,y_shield ] # Coordenadas del centro de la imagen
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



    plt.axis('off')
    plt.xticks([])
    plt.yticks([])
    matplotlib.pyplot.close(fig)
    return fig
    