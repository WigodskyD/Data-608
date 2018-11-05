
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask


url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json'
trees = pd.read_json(url)
print(trees.head(10))
print(list(trees))

firstfive_url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=5&$offset=0'
firstfive_trees = pd.read_json(firstfive_url)
print(firstfive_trees)

boro = 'Bronx'
soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' + \
            '$select=spc_common,count(tree_id)' + \
            '&$where=boroname=\'Bronx\'' + \
            '&$group=spc_common').replace(' ', '%20')
soql_trees = pd.read_json(soql_url)
soql_tree_set=str("")
for i in range(1, soql_trees.count_tree_id.count()):
    soql_tree_count=str(soql_trees.ix[i,'count_tree_id'])
    soql_trees_species=str(soql_trees.ix[i,'spc_common'])
    soql_trees_species=soql_tree_count+'  '+ soql_trees_species 
    soql_tree_set= soql_tree_set + '<br>'+soql_trees_species


app = Flask(__name__)
@app.route('/')
def main_show():
    return (soql_tree_set)

@app.route('/boro/<string:borough>')
def get_tree_data(borough):
    boro = borough
    soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' + \
                '$select=spc_common,count(tree_id)' + \
                '&$where=boroname=\'' +borough+'\'' + \
                '&$group=spc_common').replace(' ', '%20')
    soql_trees = pd.read_json(soql_url)
    return(str(soql_trees))
    