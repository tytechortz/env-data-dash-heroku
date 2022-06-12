import dash
from dash import html
from dash import dcc
from colorado_river import get_river_header, get_emptyrow

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

# Read data
# df = pd.read_csv('ftp://sidads.colorado.edu/DATASETS/NOAA/G02186/masie_4km_allyears_extent_sqkm.csv', skiprows=1)

# # Format date and set indext to date
# df['yyyyddd'] = pd.to_datetime(df['yyyyddd'], format='%Y%j')
# df.set_index('yyyyddd', inplace=True)
# df.columns = ['Total Arctic Sea', 'Beaufort Sea', 'Chukchi Sea', 'East Siberian Sea', 'Laptev Sea', 'Kara Sea',\
#      'Barents Sea', 'Greenland Sea', 'Bafin Bay Gulf of St. Lawrence', 'Canadian Archipelago', 'Hudson Bay', 'Central Arctic',\
#          'Bering Sea', 'Baltic Sea', 'Sea of Okhotsk', 'Yellow Sea', 'Cook Inlet']

# # Dropdown year selector values
# year_options = []
# for YEAR in df.index.year.unique():
#     year_options.append({'label':(YEAR), 'value':YEAR})

month_options = [
{'label':'JAN', 'value':1},
{'label':'FEB', 'value':2},
{'label':'MAR', 'value':3},
{'label':'APR', 'value':4},
{'label':'MAY', 'value':5},
{'label':'JUN', 'value':6},
{'label':'JUL', 'value':7},
{'label':'AUG', 'value':8},
{'label':'SEP', 'value':9},
{'label':'OCT', 'value':10},
{'label':'NOV', 'value':11},
{'label':'DEC', 'value':12}
]

# # Dropdown sea selector values
# sea_options = []
# for sea in df.columns.unique():
#     sea_options.append({'label':sea, 'value':sea})


def get_ice_header():

    header = html.Div([
        html.Div([
            html.H3('Arctic Sea Ice Data', style={'text-align': 'center'})
        ],
            className='row'
        ),
        html.Div([
            html.H6(
                '2006-Present',
                className='twelve columns',
                style={'text-align': 'center'}
            ),
        ],
            className='row'
        ),
        html.Div([
            html.H6(
                'Data From National Snow and Ice Data Center',
                className='twelve columns',
                style={'text-align': 'center'}
            ),
        ],
            className='row'
        ),
    ])

    return header

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
                dcc.RadioItems(
                    id='product',
                    options=[
                        {'label':'Ice Exent By Year', 'value':'years-graph'},
                        {'label':'Avg Monthy Extent', 'value':'monthly-bar'},
                        {'label':'Extent On Current Date', 'value':'extent-date'},
                        {'label':'Extent Rankings', 'value':'extent-stats'},
                        {'label':'1 Year Moving Avg', 'value':'moving-avg'},
                    ],
                    value='years-graph',
                    labelStyle={'display': 'inline'},
                    ),
            ],
                className='twelve columns'
            ),
        ],
            className='row',
                style={'background-color' : 'dark-green',
                        'box-shadow': '2px 5px 5px 1px rgba(0, 100, 0, .5)'}
        ),
    ])

    return navbar



def ice_App():
    return html.Div([
        get_ice_header(),
        get_nav_bar(),
        get_emptyrow(),
        html.Div(id='ice-graph-layout'),
        html.Div(id='monthly-extent-layout'),

        dcc.Interval(
            id='ice-interval-component',
            interval=500000, # in milliseconds
            n_intervals=0
        ),

        dcc.Store(id='ice-data'),
        dcc.Store(id='sea-options'),
        dcc.Store(id='fdta'),
        dcc.Store(id='year-options'),
        dcc.Store(id='df-monthly'),
    ])

app.layout = ice_App