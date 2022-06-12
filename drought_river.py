import dash
from dash import html
from dash import dcc
from colorado_river import get_river_header, get_emptyrow
import requests

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

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

def drought_river_App():
    return html.Div([
        get_river_header(),
        get_nav_bar(),
        get_emptyrow(),
        html.Div([
            html.H3('Colorado Drought and the Colorado River', style={'text-align': 'center'})
        ],
            className='row'
        ),
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='drought-graph'
                    )
                ],
                    className='eight columns'
                ),
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Markdown('''Moving Avg in Weeks'''),
                        ],
                            className='two columns'
                        ),
                        html.Div([
                            dcc.Input(
                                id='MA-input',
                                type='number',
                                step=1,
                                value=1
                            ),
                        ],
                            className='two columns'
                        ),
                    ],
                        className='row'
                    ),
                    html.Div([
                        html.Div([
                            html.Div(id='drought-stats'),
                        ],
                            className='twelve columns'
                        ),
                    ],
                        className='row'
                    ),
                ],
                    className='four columns'
                ),
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
                    id='drought-year',
                    min=2000,
                    max=2021,
                    # step=1,
                    marks={x: '{}'.format(x) for x in range(2000, 2022)},
                    value=[2000,2021]
                )
            ],
                className='six columns'
            ),
        ],
            className='row'
        ),
        get_emptyrow(),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='dsci-graph'
                )
            ],
                className='eight columns'
            ), 
        ],  
            className='row'
        ),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='diff-graph'
                )
            ],
                className='eight columns'
            ), 
        ],  
            className='row'
        ),
        dcc.Interval(
            id='interval-component',
            interval=500*1000, # in milliseconds
            n_intervals=0
        ),
        dcc.Store(id='drought-data'),
        # dcc.Store(id='combo-water-data'),
        # dcc.Store(id='combo-annual-change'),
    ])



app.layout = drought_river_App
