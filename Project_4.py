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

steward_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=health,steward,count(tree_id)' +\
        '&$where=boroname=\'Bronx\' AND steward != \'NaN\'' +\
        '&$group=steward,health').replace(' ', '%20')

steward_trees = pd.read_json(steward_url)
# There has to be a better way to reorder these.  Indexing didn't work.
poor = steward_trees[(steward_trees['health']=='Poor')]
fair = steward_trees[(steward_trees['health']=='Fair')]
good = steward_trees[(steward_trees['health']=='Good')]
steward_trees = pd.concat([poor, fair, good])
sum_set = steward_trees.groupby(['steward']).sum()
steward_trees= pd.merge(steward_trees,sum_set,how='left',on=['steward'])
steward_trees['percent']= steward_trees['count_tree_id_x']/steward_trees['count_tree_id_y'] * 100
print(steward_trees)
most = steward_trees[(steward_trees['steward']=='4orMore')]
three = steward_trees[(steward_trees['steward']=='3or4')]
some = steward_trees[(steward_trees['steward']=='1or2')]
zero = steward_trees[(steward_trees['steward']=='None')]

colors = {
    'background': '#efd8b1',
    'text':'red'
}


graph1 = html.Div(children=[html.H1('New York City Tree Census'),
                                dcc.Dropdown(id='boro', options=[{'label': i, 'value': i} for i in boro_choices], value='Manhattan',style = {'width':'45%','color':'red','display':'inline-block'}),
                                dcc.Dropdown(id='species', options=[{'label': j, 'value': j} for j in species_choices], value='silver maple',style = {'width':'45%','display':'inline-block'}),
                                dcc.Graph(id = 'tree_health',style={'width':'70%'})
                               ]
                      )
graph2 = html.Div(children=[dcc.Graph(id='steward_effect',style={'width':'80%'},
                              figure = {
                                   'data':  [
                                        {'x':most['health'], 'y':most['percent'], 'type':'line', 'name': '4 or more acts of stewardship'},
                                        {'x':three['health'], 'y':three['percent'], 'type':'line', 'name': '3 or 4 acts of stewardship'},
                                        {'x':some['health'], 'y':some['percent'], 'type':'line', 'name': '1 or 2 acts of stewardship'},
                                        {'x':zero['health'], 'y':zero['percent'], 'type':'line', 'name': 'no acts of stewardship'}
                                             ],
                                   'layout':{}
                                         }
                                      )])

app.layout = html.Div([graph1,graph2])
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
    'data': [{'x': health_trees['health'], 'y': health_trees['count_tree_id'], 'type': 'bar', 'name': 'Tree Health'}],
    'layout': {
        'title': str('Health of ' + species + ' Trees'),
        'plot_bgcolor': colors['background'],
        'paper_bgcolor': '#dee5f2',
        'titlefont': {'size': 46, 'color': '#788fba'},
        'font': {'size': 26}
    }
           }   

if __name__ == '__main__':
    app.run_server()

