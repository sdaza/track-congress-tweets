
# minimal example
# author: sebastian daza

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table_experiments as dt
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.plotly as py
import flask
import os
import json
import pickle
import random

import pandas as pd
from textwrap import dedent as s
from datetime import datetime
import base64

app = dash.Dash(__name__)
server = app.server
server.secret_key = os.environ.get('secret_key', 'secret')

app.title='Tracking Congress Member Tweets'

# image
image_filename = 'polarization.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# distribution plot
pol = pd.read_csv('data/tweets_pol.csv')
# pol = pol.sample(frac=0.1, replace=False)
pol = pol.groupby('month').apply(lambda x: x.sample(n=5000)) # a sample

# dropdown menus
months = ['June', 'July', 'August', 'September', 'October']
months_dict = {'June':6, 'July':7, 'August':8, 'September':9, 'October':10}
sentiment = {'Pattern':'score_pattern', 'Vader':'score_vader'}

# trend plot
avg_pattern = pd.read_csv('data/avg_pattern.csv')
avg_vader = pd.read_csv('data/avg_vader.csv')

# diff plot
models = pd.read_csv('data/models.csv')

# table tweets
tweets = pd.read_csv('data/tweets_table.csv')
tweets.rename(columns={'text':'Tweet', 'party':'Party', 'score_pattern':'Pattern', 'score_vader':'Vader'}, inplace=True)

pos_tweets = tweets.loc[tweets.Pattern > 0.60]
neg_tweets = tweets.loc[tweets.Pattern < -0.60]

# topic model
# with open("data/lda_coor.txt", "rb") as myFile:
#     lda_coor = pickle.load(myFile, encoding='latin1')
#
# with open("data/lda_tsne.txt", "rb") as myFile:
#     lda_tsne = pickle.load(myFile, encoding='latin1')
#
#
# with open("data/lda_color.txt", "rb") as myFile:
#     lda_color = pickle.load(myFile, encoding='latin1')
#
# trace = go.Scatter(
#     x=lda_tsne[:, 0],
#     y=lda_tsne[:, 1],
#     mode='markers',
#     marker=dict(
#     color=lda_color,
#     opacity=0.4),
#     hoverinfo='none'
# )
# data = [trace]
# layout = go.Layout(
#     annotations=lda_coor,
#     # width=800,
#     # height=800,
#     xaxis=dict(
#         autorange=True,
#         showgrid=False,
#         zeroline=False,
#         showline=False,
#         autotick=True,
#         ticks='',
#         showticklabels=False
#     ),
#     yaxis=dict(
#         autorange=True,
#         showgrid=False,
#         zeroline=False,
#         showline=False,
#         autotick=True,
#         ticks='',
#         showticklabels=False
#     )
# )
#
# topic_fig = go.Figure(data=data, layout=layout)

# app layout

app.layout = html.Div(children=[
            html.Div('', style={'padding': 50}),
            html.H1('Political Conflict', style={'textAlign': 'center'}),
        html.H2("Tracking sentiment of congress members' tweets",
                style={'textAlign': 'center'}),
        html.Div([
            html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))
        ], style={'textAlign': 'center'}),
        html.H5('by Sebastian Daza',
                    style={'textAlign': 'center'}),
        dcc.Markdown(s('''
        American Politics has become polarized over the past quarter-century. Research shows that American politics are more segregated and legislators have less common voting than decades ago, when senators regularly crossed the aisle to get things done. This phenomenon does not only affect politicians but also the public. According to data from the Pew Research Center, 45% of Republicans and 41% of Democrats think the other party is so dangerous that they consider it as a **threat to the nation**. Some commentators have also suggested that *media* and *new social platforms* exacerbate political polarization by spreading *fake news*.

        A polarized political environment has negative consequences, especially when the control of the executive and legislative branches are split among cohesive parties. Some of its drawbacks include the reduction of the number of compromises parties are willing to take, **less legislative productivity**, gridlocks, less policy innovation, and inhibition of the majority rule. All these consequences affects people, so it is important to look for alternative measures that help us to track political polarization.

        ## Goals:

        - Estimate polarity of tweets
          - Difference of score by party
        - Identify main topics
          - Difference of score by topic
        - *Explore the relationship between sentiment and actual votes*

        ***

        ## Sentiment Polarity by Party

        - Unsupervised approach.
        - Most of tweets are neutral.
        - No big difference by party.
        - Republicans tend to be slightly more positive.
        '''), className='container',
        containerProps={'style': {'maxWidth': '650px'}}),

        # html.Div(dcc.Markdown(text)),
        html.Div('', style={'padding': 10}), # space
        html.Label('Month', className='container', style={'maxWidth': '650px'}),
        html.Div(dcc.Dropdown(id='select-month',
                                     options=[{'label': i, 'value': i} for i in months],
                                 value='June'), className='container', style={'maxWidth': '650px'}),
        html.Div('', style={'padding': 5}), # space
        html.Label('Lexicon', className='container', style={'maxWidth': '650px'}),
        html.Div(dcc.RadioItems(id='lexicon-dist',
                         options=[{'label': 'Pattern', 'value': 'score_pattern'}, {'label': 'Vader', 'value': 'score_vader'}],
                         value='score_pattern', labelStyle={'display': 'inline-block'}), className='container', style={'maxWidth': '650px'}),
        # html.Div('', style={'padding': 10}),

        html.Div([dcc.Graph(id='density-graph', style={'margin':'auto', 'height': '600px', 'maxWidth': '900px'})]
                 ),
        html.Div('', style={'padding': 70}),
        html.H4('Positive Tweets', style={'textAlign': 'center'}),
        html.Div( dt.DataTable(
            rows=pos_tweets.to_dict('records'),
           # optional - sets the order of columns
            columns=['Tweet'],
            # row_selectable=True,
            # filterable=False,
            # sortable=True
            ), className='container', style={'maxWidth': '1000px'}),
        html.Div('', style={'padding': 110}), # space
        html.H4('Negative Tweets', style={'textAlign': 'center'}),
        html.Div( dt.DataTable(
            rows=neg_tweets.to_dict('records'),
           # optional - sets the order of columns
            columns=['Tweet'],
            # row_selectable=True,
            # filterable=False,
            # sortable=True
            ),className='container', style={'maxWidth': '1000px'}),
        html.Div('', style={'padding': 70}), # space
        dcc.Markdown(s('''
            ***

            ## Polarity over Time

            '''), className='container',
            containerProps={'style': {'maxWidth': '650px'}}),
        html.Label('Lexicon', className='container', style={'maxWidth': '650px'}),
        html.Div(dcc.RadioItems(id='lexicon-trend',
                         options=[{'label': 'Pattern', 'value': 'score_pattern'}, {'label': 'Vader', 'value': 'score_vader'}],
                         value='score_pattern', labelStyle={'display': 'inline-block'}), className='container', style={'maxWidth': '650px'}),
        html.Div([dcc.Graph(id='trend-graph',
                            style={'margin':'auto', 'height': '600px', 'maxWidth': '900px'})]),
        # dcc.Markdown(s('''
        #
        # ***
        #
        # ### What are they tweeting about?
        # #### Topic Modeling
        #
        #              '''), className='container',
        #              containerProps={'style': {'maxWidth': '650px'}}),
        # html.Div([dcc.Graph(id='topic-graph', figure=topic_fig,
        #                     style={'margin':'auto', 'height': '700px', 'maxWidth': '900px'})]),
        # html.Div('', style={'padding': 10}), # space
        dcc.Markdown(s('''

        ***

        ### Sentiment by Topic and Party

                     '''), className='container',
                     containerProps={'style': {'maxWidth': '650px'}}),
        html.Label('Number of Topics', className='container', style={'maxWidth': '500px'}),
        html.Div(dcc.Slider(id='ntopics-slider',
        min=5,
        max=20,
        marks={i: '{}'.format(i) for i in range(5,21)},
        value=15,
        ), className='container', style={'maxWidth': '500px'}),
        html.Div('', style={'padding': 20}), # space
        html.Label('Method', className='container', style={'maxWidth': '500px'}),
        html.Div(dcc.RadioItems(id='method-diff',
                         options=[{'label': 'LDA', 'value': 'lda'},
                                  {'label': 'NMF', 'value': 'nmf'}],
                         value='lda', labelStyle={'display': 'inline-block'}), className='container', style={'maxWidth': '500px'}),
        html.Label('Lexicon', className='container', style={'maxWidth': '500px'}),
        html.Div(dcc.RadioItems(id='lexicon-diff',
                         options=[{'label': 'Pattern', 'value': 'score_pattern'}, {'label': 'Vader', 'value': 'score_vader'}],
                         value='score_pattern', labelStyle={'display': 'inline-block'}), className='container', style={'maxWidth': '500px'}),
        html.Div([dcc.Graph(id='diff-graph',
                            style={'margin':'auto', 'height': '500px', 'maxWidth': '1000px'})]),
        html.Div('', style={'padding': 200}),
        dcc.Markdown(s('''
        ***

        # Next Steps

        - Labeled data and classify positive/negative tone, and confrontation
        - How well these labels predict congress members' vote?

                     '''), className='container',
                     containerProps={'style': {'maxWidth': '650px'}}),
        html.Div('', style={'padding': 50}),
        dcc.Markdown(s('''
        ***

        ##### Data

        I use data collected by the developer Alex Litel through the app ([Congressional Tweet Automator](https://github.com/alexlitel/congresstweets)). This app stores Congress member’s tweets every day, and it was highlighted recently in a [Washington Post article](https://www.washingtonpost.com/news/politics/wp/2017/06/26/how-congress-tweets-visualized/?utm_term=.6e80a8653a5f).
                     '''), className='container',
                     containerProps={'style': {'maxWidth': '650px'}})
            ])

@app.callback(
    dash.dependencies.Output('density-graph', 'figure'),
    [dash.dependencies.Input('select-month', 'value'),
     dash.dependencies.Input('lexicon-dist','value')])

def update_density_graph(month_value, sentiment):
    dist_r = pol.loc[(pol.month==months_dict[month_value]) & (pol.party=='R'), sentiment]
    dist_d = pol.loc[(pol.month==months_dict[month_value]) & (pol.party=='D'), sentiment]
    hist_data = [dist_r, dist_d]
    group_labels = ['Republican', 'Democrat']
    fig_dens = ff.create_distplot(hist_data, group_labels,
                                colors =['red', 'blue'],
                                show_hist=False)

    fig_dens['layout'].update(legend=dict(orientation="h", x=0.35, y=1.2))
    return fig_dens

@app.callback(
    dash.dependencies.Output('trend-graph', 'figure'),
    [dash.dependencies.Input('lexicon-trend','value')])

def update_trend_graph(sentiment):
    #print(sentiment)
    if (str(sentiment) == 'score_pattern'):
        avg_d = avg_pattern.loc[avg_pattern.party=='D', ['date', sentiment]]
        avg_r = avg_pattern.loc[avg_pattern.party=='R', ['date', sentiment]]
        avg_d.rename(columns= {'score_pattern':'polarity'}, inplace=True)
        avg_r.rename(columns= {'score_pattern':'polarity'}, inplace=True)
        #print(avg_d.head())
    else:
        avg_d = avg_vader.loc[avg_vader.party=='D', ['date', sentiment]]
        avg_r = avg_vader.loc[avg_vader.party=='R', ['date', sentiment]]
        avg_d.rename(columns= {'score_vader':'polarity'}, inplace=True)
        avg_r.rename(columns= {'score_vader':'polarity'}, inplace=True)

    r = go.Scatter(x=avg_r.date, y=avg_r.polarity, name = 'Republican',
                line = dict(color = 'red'),
                opacity = 0.8)

    d = go.Scatter(x=avg_d.date, y=avg_d.polarity, name = 'Democrat',
                line = dict(color = 'blue'),
                opacity = 0.8)

    data = [r, d]

    layout_pattern = go.Layout(
        showlegend=True,
        title='Sentiment Polarity Score by Party',
        annotations=[
        dict(
            x=pd.to_datetime('2017-07-04'),
            y=0.53,
            xref='x',
            yref='y',
            text='July 4th',
            showarrow=True,
            ax=0,
            ay=-40
        ),
        dict(
            x=pd.to_datetime('2017-08-12'),
            y=0.23,
            xref='x',
            yref='y',
            text='Charlottesville rally',
            showarrow=True,
            ax=0,
            ay=-40
        ),
        dict(
            x=pd.to_datetime('2017-10-02'),
            y=0.25,
            xref='x',
            yref='y',
            text='Las Vegas shooting',
            showarrow=True,
            ax=0,
            ay=-40
        ),
        dict(
            x=pd.to_datetime('2017-07-26'),
            y=0.28,
            xref='x',
            yref='y',
            text='Health Care Repeal',
            showarrow=True,
            ax=0,
            ay=-40
        )
        ]
        )

    layout_vader = go.Layout(
            showlegend=True,
            title='Sentiment Polarity Score by Party',
            annotations=[
            dict(
                x=pd.to_datetime('2017-07-04'),
                y=0.7,
                xref='x',
                yref='y',
                text='July 4th',
                showarrow=True,
                ax=0,
                ay=-40
            ),
            dict(
                x=pd.to_datetime('2017-08-12'),
                y=0.55,
                xref='x',
                yref='y',
                text='Charlottesville rally',
                showarrow=True,
                ax=0,
                ay=-40
            ),
            dict(
                x=pd.to_datetime('2017-10-02'),
                y=0.5,
                xref='x',
                yref='y',
                text='Las Vegas shooting',
                showarrow=True,
                ax=0,
                ay=-40
            ),
            dict(
                x=pd.to_datetime('2017-07-26'),
                y=0.45,
                xref='x',
                yref='y',
                text='Health Care Repeal',
                showarrow=True,
                ax=0,
                ay=-40
            )
            ]
            )

    if (sentiment=='score_pattern'):
        fig_trend = go.Figure(data=data, layout=layout_pattern)
    else:
        fig_trend = go.Figure(data=data, layout=layout_vader)

    fig_trend['layout'].update(legend=dict(orientation="h", x=0.35, y=1.1))
    return fig_trend

@app.callback(
    dash.dependencies.Output('diff-graph', 'figure'),
    [dash.dependencies.Input('ntopics-slider','value'),
     dash.dependencies.Input('method-diff','value'),
     dash.dependencies.Input('lexicon-diff','value')])

def update_diff_graph(ntopics, method, lexicon):
    if method == 'lda':
        m = models.loc[models.model=='lda']
    else:
        m = models.loc[models.model=='nmf']

    if lexicon=='score_pattern':
        m = m.sort_values(by='diff_pattern', ascending=True)
        diff = m.loc[m.model==method, 'diff_pattern']
    else:
        m = m.sort_values(by='diff_vader', ascending=True)
        diff = m.loc[m.model==method, 'diff_vader']

    words = m['words']

    # get words and scores
# trace0 = go.Bar(
#     x=y_saving,
#     y=x_saving,
#     marker=dict(
#         color='rgba(50, 171, 96, 0.6)',
#         line=dict(
#             color='rgba(50, 171, 96, 1.0)',
#             width=1),
#     ),
#     name='Household savings, percentage of household disposable income',
#     orientation='h',
# )
    data = go.Bar(
        x=diff[-ntopics:],
        y=words[-ntopics:],
        marker=dict(
        color='rgba(50, 171, 96, 0.6)',
        line=dict(
            color='rgba(50, 171, 96, 1.0)',
            width=1)),
            orientation='h'
        )

    # data = [trace0, trace1]
    layout = go.Layout(
       title="Difference Polarity between Parties",
            xaxis=dict(
            showgrid=False,
            zeroline = False,
            showline=False,
            linecolor='rgb(102, 102, 102)',
            titlefont=dict(
                color='rgb(204, 204, 204)'
            ),
            tickfont=dict(
                color='rgb(102, 102, 102)',
            ),
            autotick=False,
            dtick=10,
            ticks='outside',
            tickcolor='rgb(102, 102, 102)',
        ),
        margin=dict(
            l=600,
            r=5,
            b=50,
            t=40
        ),
        width=1000,
        height=600,
    )
    fig_diff = go.Figure(data=[data], layout=layout)
    # fig_diff['layout'].update(legend=dict(orientation="h", x=0.70, y=1.05))
    return fig_diff

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium"]


for css in external_css:
    app.css.append_css({"external_url": css})


if __name__ == '__main__':
    app.run_server(debug=True)
