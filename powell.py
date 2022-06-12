import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import time
import json
import requests
from datetime import datetime, date, timedelta
import flask
from datetime import datetime as dt
import csv

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

def get_powell_header():

    header = html.Div([

        # html.Div([], className = 'col-2'), #Same as img width, allowing to have the title centrally aligned

        html.Div([
            html.H2(
                'Lake Powell Details',
                className='twelve columns',
                style={'text-align': 'center'}
            ),
        ],
            className='row'
        ),
    ])

    return header

def get_emptyrow(h='15px'):
    """This returns an empty row of a defined height"""

    emptyrow = html.Div([
        html.Div([
            html.Br()
        ], className = 'col-12')
    ],
    className = 'row',
    style = {'height' : h})

    return emptyrow

def get_nav_bar():
    navbar = html.Div([
        html.Div([
            html.Div([], className='col-2'),
            html.Div([
                dcc.Link(
                    html.H6(children='Home'),
                    href='/homepage'
                )
            ],
                className='col-2',
                style={'text-align': 'center'}
            ),
            html.Div([], className = 'col-2')
        ],
            className = 'row',
            style = {'background-color' : 'dark-green',
                    'box-shadow': '2px 5px 5px 1px rgba(0, 100, 0, .5)'}
        ),
        html.Div([
            html.Div([
                html.Div([
                    dcc.Link(
                        html.H6(children='Mead and Powell'),
                        href='/colorado-river'
                    )
                ],
                    className='six columns',
                    style={'text-align': 'center'}
                ),
                html.Div([
                    dcc.Link(
                        html.H6(children='Upper Reservoirs'),
                        href='/ur'
                    )
                ],
                    className='six columns',
                    style={'text-align': 'center'}
                ),
            ],
                className='twelve columns'
            ),
        ],
            className = 'row',
                style = {'background-color' : 'dark-green',
                        'box-shadow': '2px 5px 5px 1px rgba(0, 100, 0, .5)'}
        ),

    ])

    return navbar

def lake_powell_App():
    return html.Div([
        get_powell_header(),
        get_nav_bar(),
        get_emptyrow(),
        html.Div([
            html.Div([
                dcc.Graph(id='powell-graph')
            ],
                className='twelve columns'
            ),
        ],
            className='row'
        ),
        html.Div([
            html.Div([], className='one column'),
            html.Div([
                dcc.RangeSlider(
                    id='powell-year',
                    min=2000,
                    max=2021,
                    # step=1,
                    marks={x: '{}'.format(x) for x in range(2000, 2022)},
                    value=[2000,2021]
                )
            ],
                className='ten columns'
            ),
        ],
            className='row'
        ),
        html.Div(id='powell-stats')
    ])

app.layout = lake_powell_App