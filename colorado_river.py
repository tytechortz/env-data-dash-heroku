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




capacities = {'Lake Powell Glen Canyon Dam and Powerplant': 24322000, 'Lake Mead Hoover Dam and Powerplant': 26134000, 'FLAMING GORGE RESERVOIR': 3788700, 'NAVAJO RESERVOIR': 1708600, 'BLUE MESA RESERVOIR': 940800, 'Powell Mead Combo': 50456000, 'UR': 6438100}


def get_river_header():

    header = html.Div([

        # html.Div([], className = 'col-2'), #Same as img width, allowing to have the title centrally aligned

        html.Div([
            html.H2(
                'Colorado River Water Storage',
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
                        html.H6(children='Upper Reservoirs'),
                        href='/ur'
                    )
                ],
                    className='six columns',
                    style={'text-align': 'center'}
                ),
                html.Div([
                    dcc.Link(
                        html.H6(children='Drought'),
                        href='/drought-river'
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
    

def river_App():
    return html.Div([
        get_river_header(),
        get_nav_bar(),
        get_emptyrow(),
        html.Div([
            html.Div([
                dcc.Loading(
                id="loading-powell",
                type="default",
                children=html.Div(dcc.Graph(id='powell-levels'))),
            ],
                className='six columns'
            ),
            html.Div([
                dcc.Graph(
                    id='powell-annual-changes'
                )
            ],
                className='six columns'
            ),
        ],
            className='row'
        ),
        html.Div([
            html.Div([
                dcc.Loading(
                id="loading-mead",
                type="default",
                children=html.Div(dcc.Graph(id='mead-levels'))),
            ],
                className='six columns'
            ),
            html.Div([
                dcc.Graph(
                    id='mead-annual-changes'
                )
            ],
                className='six columns'
            ),
        ],
            className='row'
        ),
        html.Div([
            html.Div([
                dcc.Loading(
                id="loading-combo",
                type="default",
                children=html.Div(dcc.Graph(id='combo-levels'))),
            ],
                className='six columns'
            ),
            html.Div([
                dcc.Graph(
                    id='combo-annual-changes'
                )
            ],
                className='six columns'
            ),
        ],
            className='row'
        ),
        html.Div([
            html.Div([], className='one column'),
            html.Div([
                html.H6('Current Storage - AF', style={'text-align': 'center'})
            ],
                className='two columns'
            ),
            html.Div([
                html.H6('Pct. Full', style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('24 hr', style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('10 Day', style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('C.Y.', style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('Year', style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('Rec Low', style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('Diff', style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('Rec Low Date', style={'text-align': 'center'})
            ],
                className='two columns'
            ),
        ],
            className='row'
        ),
        html.Div([
            html.Div(id='cur-levels')
        ],
            className='row'
        ),
        # html.Div([
            # html.Div([
            #     dcc.Graph(
            #         id='powell-annual-changes'
            #     )
            # ],
            #     className='four columns'
            # ),
            # html.Div([
            #     dcc.Graph(
            #         id='mead-annual-changes'
            #     )
            # ],
            #     className='four columns'
            # ),
            # html.Div([
            #     dcc.Graph(
            #         id='combo-annual-changes'
            #     )
            # ],
            #     className='four columns'
            # ),
            
        # ],
        #     className='row'
        # ),
        html.Div([
            html.Div([
                dcc.Link(
                    html.H6(children='Lake Powell'),
                    href='/powell'
                )
            ],
                className='four columns',
                style={'text-align': 'center'}
            ),
        ],
            className='row'
        ),
        dcc.Interval(
        id='interval-component',
        interval=500*1000, # in milliseconds
        n_intervals=0
        ),
        # dcc.Store(id='powell-water-data'),
        dcc.Store(id='powell-water-data-raw'),
        dcc.Store(id='mead-water-data'),
        dcc.Store(id='mead-water-data-raw'),
        # dcc.Store(id='combo-water-data'),
        dcc.Store(id='powell-annual-change'),
        dcc.Store(id='mead-annual-change'),
        # dcc.Store(id='combo-annual-change'),
    ])



app.layout = river_App