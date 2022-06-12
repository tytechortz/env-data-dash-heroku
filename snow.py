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
def get_snow_header():

    header = html.Div([

        # html.Div([], className = 'col-2'), #Same as img width, allowing to have the title centrally aligned

        html.Div([
            html.H2(
                'Colorado Snowpack Data',
                className='twelve columns',
                style={'text-align': 'center'}
            ),
        ],
            className='row'
        ),
    ])

    return header

def snow_App(): 
    return html.Div([
        get_snow_header(),
        get_nav_bar(),
        html.Div([
            html.Div([
                html.Div([ 
                    html.H2(),
                ],
                    className='one column'
                ),
                html.Div([
                    html.H6('Select River Basin', style={'text-align': 'left'})
                ],
                    className='three columns'
                ),
                
            ],
                className='twelve columns'
            ),      
        ],
            className='row'
        ),
        html.Div([
            html.Div([ 
                    html.H2(),
                ],
                    className='one column'
                ),
            html.Div([
                dcc.Dropdown(
                    id = 'river-basin',
                    options = [
                        {'label': 'Arkansas', 'value': 'arkansas'},
                        {'label': 'Colorado', 'value': 'colorado_headwaters'},
                        {'label': 'Gunnison', 'value': 'gunnison'},
                        {'label': 'Laramie/N. Platte', 'value': 'laramie_and_north_platte'},
                        {'label': 'Rio Grande', 'value': 'upper_rio_grande'},
                        {'label': 'San Juan', 'value': 'san_miguel-dolores-animas-san_juan'},
                        {'label': 'South Platte', 'value': 'south_platte'},
                        {'label': 'Yampa', 'value': 'yampa-white-little_snake'},
                        {'label': 'State of Colorado', 'value': 'state_of_colorado'},
                    ],
                    value = 'state_of_colorado',
                )
            ],
                className='two columns'
            ),
        ],
            className='row'
        ),
        html.Div([
            html.Div([
                dcc.Graph(id='snow-graph'),
            ],
                className='eight columns'
            ),
            html.Div([
                html.Div(id='snowpack-stats'),
            ],
                className='four columns'
            ),
        ],
            className='row'
        ),
        html.Div([
            html.Div([ 
                    html.H2(),
                ],
                    className='one column'
                ),
            html.Div([
                html.Div(id='snow-year-selector'),
            ],
                className='four columns'
            ),
        ],
            className='row'
        ),
        html.Div([
            html.Div([
                dcc.Graph(id='snow-daily-pct')
            ],
                className='eight columns'
            ),
            html.Div([
                html.Div(id='snow-daily-pct-stats'),
            ],
                className='four columns'
            ),
        ],
            className='row'
        ),
        html.Div([
            dcc.Interval(
                id='snow-interval-component',
                interval=300000,
                n_intervals=0
            ),
        ]),
        dcc.Store(id='snow-data-raw'),
        dcc.Store(id='snow-year-options'),
]) 

app.layout = snow_App