import dash
from dash import html
from dash import dcc
from colorado_river import get_river_header, get_emptyrow

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
                    dcc.RadioItems(
                    id='product',
                    options=[
                        {'label':'Temperature graphs', 'value':'temp-graph'},
                        {'label':'Climatology for a day', 'value':'climate-for-day'},
                        {'label':'Full Record Bar Graphs', 'value':'frbg'},
                        {'label':'5 Year Moving Avgs', 'value':'fyma-graph'},
                        {'label':'Full Record Heat Map', 'value':'frhm'},
                        {'label':'Annual Rankings', 'value':'temp-annual-ranks'},
                    ],
                    value='temp-graph',
                    labelStyle={'display': 'inline'},
                    ),
                ],
                    className='pretty_container'
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

def get_temp_header():

    header = html.Div([
        html.Div([
            html.H3('Denver Central Park Climate Data', style={'text-align': 'center'})
        ],
            className='row'
        ),
        html.Div(id='date-title'),
    ])

    return header

def dt_App():
    return html.Div([
        get_temp_header(),
        get_nav_bar(),
        get_emptyrow(),
        html.Div([
       
        ],
            className='row'
        ),
        html.Div(id='temp-graph-layout'),
        html.Div(id='climate-layout'),
        html.Div(id='frbg-layout'),
        html.Div(id='fyma-layout'),
        # html.Div(id='date-picker'),
        # dcc.Graph(id='temp-graph'),
        dcc.Interval(
            id='interval-component',
            interval=500*1000, # in milliseconds
            n_intervals=0
        ),
        dcc.Store(id='temp-data'),
        dcc.Store(id='rec-highs'),
        dcc.Store(id='rec-lows'),
        dcc.Store(id='temps'),
        dcc.Store(id='d-max-max'),
        dcc.Store(id='avg-of-dly-highs'),
        dcc.Store(id='d-min-max'),
        dcc.Store(id='d-min-min'),
        dcc.Store(id='avg-of-dly-lows'),
        dcc.Store(id='d-max-min'),
        dcc.Store(id='layout'),
        dcc.Store(id='all-data'),
        dcc.Store(id='all-temps'),
        dcc.Store(id='climate-data'),
        dcc.Store(id='df5'),
        dcc.Store(id='max-trend'),
        dcc.Store(id='min-trend'),
])

app.layout = dt_App