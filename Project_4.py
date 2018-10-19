import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
app = dash.Dash('TheApp')
server = app.server



url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json'
trees = pd.read_json(url)
print(trees.head(10))
print(list(trees))

firstfive_url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=5&$offset=0'
firstfive_trees = pd.read_json(firstfive_url)
print(firstfive_trees)

boro = 'Bronx'
soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=spc_common,count(tree_id)' +\
        '&$where=boroname=\'Bronx\'' +\
        '&$group=spc_common').replace(' ', '%20')
soql_trees = pd.read_json(soql_url)

print(soql_trees)

boro = 'Brooklyn'
species = 'Cornelian cherry'
health_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=health,count(tree_id)' +\
        '&$where=health!=\'NaN\' AND boroname=\'' + boro + '\'AND spc_common=\'' + species + '\'' +\
        '&$group=health').replace(' ', '%20')
health_trees = pd.read_json(health_url)

print(health_trees)
species_choices = soql_trees['spc_common'].unique()
boro_choices = ('Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island')
plt.bar(health_trees['health'], health_trees['count_tree_id'])

graph1 = html.Div(children=[html.H1('New York City Tree Census'),
                                dcc.Dropdown(id='boro', options=[{'label': i, 'value': i} for i in boro_choices], value='Manhattan',style = {'width':'45%','color':'#788fba','display':'inline-block'}),
                                dcc.Dropdown(id='species', options=[{'label': j, 'value': j} for j in species_choices], value='silver maple',style = {'width':'45%','color':'#788fba','display':'inline-block'}),
                                dcc.Graph(id = 'tree_health',style={'width':'70%'})
                               ]
                      )
graph2 = html.Div(children=[
                                dcc.Dropdown(id='boroB', options=[{'label': i, 'value': i} for i in boro_choices], value='Brooklyn',style = {'width':'45%','color':'#52682d','display':'inline-block'}),
                                dcc.Dropdown(id='speciesB', options=[{'label': j, 'value': j} for j in species_choices], value='silver maple',style = {'width':'45%','color':'#52682d','display':'inline-block'}),
                                dcc.Graph(id='steward_effect',style={'width':'70%'})
                                ]
                      )


app.layout = html.Div([graph1, graph2])
@app.callback(
    dash.dependencies.Output('tree_health', 'figure'),
    [dash.dependencies.Input('boro', 'value'),
     dash.dependencies.Input('species', 'value')])
def update_figure(boro, species):
    health_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' + \
                  '$select=health,count(tree_id)' + \
                  '&$where=health!=\'NaN\' AND boroname=\'' + boro + '\'AND spc_common=\'' + species + '\'' + \
                  '&$group=health').replace(' ', '%20')
    health_trees = pd.read_json(health_url)
    
    return{
    'data': [{'x': ['Poor','Fair','Good'], 'y': health_trees['count_tree_id'], 'type': 'bar', 'name': 'Tree Health'}],
    'layout': {
        'title': str('Health of ' + species + ' Trees'),
        'plot_bgcolor': '#eaf2f7',
        'paper_bgcolor': '#dee5f2',
        'titlefont': {'size': 46, 'color': '#788fba'},
        'font': {'size': 26},
        'marker':"{'color':['red','blue','white']}"
    }
           }


@app.callback(
    dash.dependencies.Output('steward_effect', 'figure'),
    [dash.dependencies.Input('boroB', 'value'),
     dash.dependencies.Input('speciesB', 'value')])
def update_figure(boroB, speciesB):
    steward_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' + \
                   '$select=health,steward,count(tree_id)' + \
                   '&$where=boroname=\''  + boroB + '\' AND steward != \'NaN\' AND spc_common=\'' + speciesB + '\'' + \
                   '&$group=steward,health').replace(' ', '%20')

    steward_trees = pd.read_json(steward_url)
    sum_set = steward_trees.groupby(['steward']).sum()
    steward_trees = pd.merge(steward_trees, sum_set, how='left', on=['steward'])
    steward_trees['percent'] = steward_trees['count_tree_id_x'] / steward_trees['count_tree_id_y'] * 100


    most = steward_trees[(steward_trees['steward'] == '4orMore')]
    three = steward_trees[(steward_trees['steward'] == '3or4')]
    some = steward_trees[(steward_trees['steward'] == '1or2')]
    zero = steward_trees[(steward_trees['steward'] == 'None')]
    return {
        'data': [
            {'x': ['Poor','Fair','Good'], 'y': most['percent'], 'type': 'line', 'name': '4 or more acts of stewardship','line':{'color':'#354a36','width':'5'}},
            {'x': ['Poor','Fair','Good'], 'y': three['percent'], 'type': 'line', 'name': '3 or 4 acts of stewardship','line':{'color':'#52682d','width':'3'}},
            {'x': ['Poor','Fair','Good'], 'y': some['percent'], 'type': 'line', 'name': '1 or 2 acts of stewardship','line':{'color':'#6e8b3d'}},
            {'x': ['Poor','Fair','Good'], 'y': zero['percent'], 'type': 'line', 'name': 'no acts of stewardship','line':{'color':'#7c9d45','width':'1.5'}}],
        'layout': {
            'title': str('Effect of Stewardship on ' + speciesB + ' Trees'),
            'plot_bgcolor': '#e9ede8',
            'paper_bgcolor': '#ddeada',
            'titlefont': {'size': 46, 'color': '#354a36'},
            'font': {'size': 26}
        }
    }

if __name__ == '__main__':
    app.run_server()
