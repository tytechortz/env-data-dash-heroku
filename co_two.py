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
    ])

    return navbar

def get_co2_header():

    header = html.Div([

        # html.Div([], className = 'col-2'), #Same as img width, allowing to have the title centrally aligned

        html.Div([
            html.H2(
                'Atmospheric CO2',
                className='twelve columns',
                style={'text-align': 'center'}
            ),
        ],
            className='row'
        ),
    ])

    return header

def co2_App():
    return html.Div([
        get_co2_header(),
        get_nav_bar(),
        get_emptyrow(),
        html.Div([
            html.Div([
                html.H3('Atmospheric CO2 Concentration', style={'text-align': 'center'})
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='co2-levels',
                        # figure=fig
                    ),
                ],
                    className='nine columns'
                ),
                html.Div([
                    html.Div(id='total-co2-stats'),
                # html.Div([
                #     html.Div(id='max-co2-layout'),
                #     html.Div(id='current-co2-layout'),
                #     html.Div(id='avg-co2-layout'),
                ],
                    className='three columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    html.H6('Select month to view data for last 2 years for selected month.')
                    ],
                        className='row'
                    ),
                html.Div([
                    dcc.Dropdown(
                        id = 'CO2-month',
                        options = [
                            {'label': 'JAN', 'value': 1},
                            {'label': 'FEB', 'value': 2},
                            {'label': 'MAR', 'value': 3},
                            {'label': 'APR', 'value': 4},
                            {'label': 'MAY', 'value': 5},
                            {'label': 'JUN', 'value': 6},
                            {'label': 'JUL', 'value': 7},
                            {'label': 'AUG', 'value': 8},
                            {'label': 'SEP', 'value': 9},
                            {'label': 'OCT', 'value': 10},
                            {'label': 'NOV', 'value': 11},
                            {'label': 'DEC', 'value': 12},
                        ],
                        value = 1,
                    )
                ],
                    className='two columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='monthly-co2-levels',
                        # figure=fig
                    ),
                ],
                    className='nine columns'
                ),
                html.Div([
                    html.Div(id='monthly-co2-stats'),
                ],
                    className='three columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                dcc.Interval(
                    id='CO2-interval-component',
                    interval=3000000,
                    n_intervals=0
                ),
            ]),
        ]),
        dcc.Store(id='CO2-data'),
        dcc.Store(id='CO2-month-data'),
    ])



app.layout = co2_App