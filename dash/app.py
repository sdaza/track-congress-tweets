
# minimal example
# author: sebastian daza

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import flask
import plotly.graph_objs as go
import os
import numpy as np
import pandas as pd


server = flask.Flask('congress')
app = dash.Dash('congress', server=server, csrf_protect=False)
server.secret_key = os.environ.get('secret_key', 'secret')
app.title='Tracking Congress Member Tweets'

@server.route('/data/<path:path>')
def serve_static(path):
    root_dir = os.getcwd()
    return flask.send_from_directory(os.path.join(root_dir, 'data'), path)

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })

# get data
pol = pd.read_csv('data/tweets_pol.csv')


# app.css.config.serve_locally = False
# app.scripts.config.serve_locally = False

# app.css.append_css(
#         {"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

text = '''
# Goals
1. Estimate polarity of tweets
    - Explore fifferences of score by party

2. Identify main topics
    - What are the most controversial topics
3. Explore the relationship between sentiment and actual votes
'''


months = ['June', 'July', 'August', 'September', 'October']


app.layout = html.Div(children=[
        html.H1(children='Political Conflict', style={'textAlign': 'center'}),
        html.H2(children="Tracking sentiment of congress members' tweets",
                style={'textAlign': 'center'}),
        dcc.Dropdown(id='month',
                         options=[{'label': i, 'value': i} for i in months],
                         value='July'),
        dcc.Graph(id='density')
            ])

@app.callback(
    dash.dependencies.Output('density', 'figure'),
    dash.dependencies.Input('month', 'value'))

def update_graph(month):
    dist_r = pol.loc[(pol.month==month_value) & (pol.party=='R'), 'polarity']
    dist_d = pol.loc[(pol.month==month_value) & (pol.party=='D'), 'polarity']
    hist_data = [dist_r, dist_d]
    group_labels = ['Republican', 'Democrat']

    return {
        'data': [go.Distplot(hist_data, group_labels, colors=['red', 'blue'])]
    }




# app.layout = html.Div(children=[
#
#
#             html.H1(children='Political Conflict', style={'textAlign': 'center'}),
#
#             html.H2(children="Tracking sentiment of congress members' tweets",
#                 style={'textAlign': 'center'}),
#
#             html.Div(dcc.Markdown(children=text)),
#
#             html.Div([dcc.Graph(
#                 id='example-graph',
#                 figure={
#                         'data':[
#                                 {'x':[1,2,3], 'y':[4,1,2], 'type':'bar', 'name':'SF'},
#                                 {'x': [1,2,3], 'y':[2,4,5], 'type':'bar', 'name':'Montreal'}
#                             ],
#                         'layout': {
#                                 'title': 'Bar Plot'
#                                     }
#                     }, style={'width': '48%'}
#             ),
#     ])
#         ]
#
# )


# @app.server.route('/static/<path:path>')
# def static_file(path):
#     static_folder = os.path.join(os.getcwd(), 'static')
#     return send_from_directory(static_folder, path)

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/0e463810ed36927caf20372b6411690692f94819/dash-drug-discovery-demo-stylesheet.css"]


for css in external_css:
    app.css.append_css({"external_url": css})


if __name__ == '__main__':
    app.run_server()
