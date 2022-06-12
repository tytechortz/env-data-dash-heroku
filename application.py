
import dash
from dash import dcc
from dash import html
from dash import dash_table as dt
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from homepage import Homepage
import time
from colorado_river import river_App, capacities
from upper_res import ur_App
from drought_river import drought_river_App
from denver_temps import dt_App
from co_two import co2_App
from ice import ice_App, month_options
from snow import snow_App
from powell import lake_powell_App
import pandas as pd
from numpy import arange,array,ones
from scipy import stats
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
from datetime import datetime, date, timedelta
import requests
import io


today = time.strftime("%Y-%m-%d")
# yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
# cur_mo_day = time.strftime("%m-%d")
# yes_mo_day = yesterday[5:]
# print(yes_mo_day)
# yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
two_days_ago = datetime.strftime(datetime.now() - timedelta(2), '%Y-%m-%d')
current_year = datetime.now().year
current_month = datetime.now().month
startyr = 1950
year_count = current_year-startyr
# print(today)
value_range = [0, 365]

app = dash.Dash(name=__name__, 
                title="Environmental Data Dashboard",
                assets_folder="static",
                assets_url_path="static")

application = app.server

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content'),
    dcc.Store(id='combo-annual-change', storage_type='session'),
    dcc.Store(id='combo-water-data', storage_type='memory'),
    # dcc.Store(id='powell-water-data-raw'),
    dcc.Store(id='powell-water-data', storage_type='memory'),
    dcc.Store(id='temps', storage_type='session'),
    dcc.Store(id='graph-data', storage_type='session'),
    dcc.Store(id='cur-mo-day', storage_type='session'),
    dcc.Store(id='yes-mo-day', storage_type='session'),
    dcc.Store(id='yesterday', storage_type='session'),
    dcc.Store(id='today', storage_type='session'),
    dcc.Interval(
            id='interval-component',
            interval=500*1000, # in milliseconds
            n_intervals=0
        ),
])

@app.callback(
    [Output('cur-mo-day', 'data'),
    Output('yes-mo-day', 'data'),
    Output('yesterday', 'data'),
    Output('today', 'data')],
    Input('interval-component', 'n_intervals'))
def get_cur_day(n):
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    cur_mo_day = time.strftime("%m-%d")
    yes_mo_day = yesterday[5:]
    today = time.strftime("%Y-%m-%d")

    return cur_mo_day, yes_mo_day, yesterday, today

powell_data_url= 'https://data.usbr.gov/rise/api/result/download?type=csv&itemId=509&before=' + today + '&after=1999-12-30&filename=Lake%20Powell%20Glen%20Canyon%20Dam%20and%20Powerplant%20Daily%20Lake%2FReservoir%20Storage-af%20Time%20Series%20Data%20(2021-12-01%20-%202021-12-12)&order=ASC'

# https://data.usbr.gov/rise/api/result/download?type=csv&itemId=509&before=2021-12-14&after=1999-12-30&filename=Lake%20Powell%20Glen%20Canyon%20Dam%20and%20Powerplant%20Daily%20Lake%2FReservoir%20Storage-af%20Time%20Series%20Data%20

mead_data_url = 'https://data.usbr.gov/rise/api/result/download?type=csv&itemId=6124&before=' + today + '&after=1999-12-30&filename=Lake%20Mead%20Hoover%20Dam%20and%20Powerplant%20Daily%20Lake%2FReservoir%20Storage-af%20Time%20Series%20Data%20(1937-05-28%20-%202020-11-30)&order=ASC'

# https://data.usbr.gov/rise/api/result/download?type=csv&itemId=6124&before=2021-12-04&after=1999-12-30&filename=Lake%20Mead%20Hoover%20Dam%20and%20Powerplant%20Daily%20Lake%2FReservoir%20Storage-af%20Time%20Series%20Data%20(1937-05-28%20-%202020-11-30)&order=ASC

blue_mesa_data_url = 'https://data.usbr.gov/rise/api/result/download?type=csv&itemId=76&before=' + today + '&after=1999-12-30&filename=Blue%20Mesa%20Reservoir%20Dam%20and%20Powerplant%20Daily%20Lake%2FReservoir%20Storage-af%20Time%20Series%20Data%20(2000-01-01%20-%202021-07-14)&order=ASC'

# https://data.usbr.gov/rise/api/result/download?type=csv&itemId=76&before=2021-11-15&after=1999-12-30&filename=Blue%20Mesa%20Reservoir%20Dam%20and%20Powerplant%20Daily%20Lake%2FReservoir%20Storage-af%20Time%20Series%20Data%20(2000-01-01%20-%202021-07-14)&order=ASC

navajo_data_url = 'https://data.usbr.gov/rise/api/result/download?type=csv&itemId=613&before=' + today + '&after=1999-12-30&filename=Navajo%20Reservoir%20and%20Dam%20Daily%20Lake%2FReservoir%20Storage-af%20Time%20Series%20Data%20(1999-12-31%20-%202021-07-14)&order=ASC'

fg_data_url = 'https://data.usbr.gov/rise/api/result/download?type=csv&itemId=337&before=' + today + '&after=1999-12-30&filename=Flaming%20Gorge%20Reservoir%20Dam%20and%20Powerplant%20Daily%20Lake%2FReservoir%20Storage-af%20Time%20Series%20Data%20(1999-12-31%20-%202021-07-15)&order=ASC'

blue_mesa_data_raw = pd.read_csv(blue_mesa_data_url)
navajo_data_raw = pd.read_csv(navajo_data_url)
fg_data_raw = pd.read_csv(fg_data_url)






today = time.strftime("%Y-%m-%d")
today2 = datetime.now()
year = datetime.now().year
f_date = datetime(year, 1, 1)
delta = today2 - f_date
days = delta.days

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/den-temps':
        return dt_App()
    elif pathname == '/ice':
        return ice_App()
    elif pathname == '/colorado-river':
        return river_App()
    elif pathname == '/ur':
        return ur_App()
    elif pathname == '/drought-river':
        return drought_river_App()
    elif pathname == '/co2':
        return co2_App()
    elif pathname == '/snow':
        return snow_App()
    elif pathname == '/powell':
        return lake_powell_App()
    else:
        return Homepage()


def get_navbar(p = 'homepage'):
    navbar_homepage = html.Div([
        html.Div([], className='col-2'),
        html.Div([
            dcc.Link(
                html.H6(children='Upper Reservoirs'),
                href='/ur'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([
            dcc.Link(
                html.H6(children='Drought'),
                href='/drought-river'
            )
        ],
            className='col-2',
            style={'text-align': 'center'}
        ),
        html.Div([], className = 'col-2'),
    ],
    className = 'row',
    style = {'background-color' : 'dark-green',
            'box-shadow': '2px 5px 5px 1px rgba(0, 100, 0, .5)'}
    )
    non_home = html.Div([
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
    )
    if p == 'homepage':
        return navbar_homepage
    else:
        return non_home

@app.callback(
    Output('powell-water-data-raw', 'data'),
    Input('interval-component', 'n_intervals'))
def get_powell_data(n):
    powell_data_raw = pd.read_csv(powell_data_url)
    # print(powell_data_raw)
    return powell_data_raw.to_json()

@app.callback(
    Output('mead-water-data-raw', 'data'),
    Input('interval-component', 'n_intervals'))
def get_mead_data(n):
    mead_data_raw = pd.read_csv(mead_data_url)
    # print(powell_data_raw)
    return mead_data_raw.to_json()


@app.callback([
    Output('powell-water-data', 'data'),
    Output('mead-water-data', 'data'),
    Output('combo-water-data', 'data'),],
    [Input('interval-component', 'n_intervals'),
    Input('powell-water-data-raw', 'data'),
    Input('mead-water-data-raw', 'data')])
def clean_powell_data(n, powell_data_raw, mead_data_raw):
    df_powell_water = pd.read_json(powell_data_raw)
    # print(df_powell_water)
    df_powell_water = df_powell_water.drop(df_powell_water.columns[[1,3,4,5,7,8]], axis=1)
    
    df_powell_water.columns = ["Site", "Water Level", "Date"]
    
    df_powell_water = df_powell_water[8:]
    
    df_powell_water['power level'] = 6124000
    df_powell_water['sick pool'] = 4158000
    df_powell_water['dead pool'] = 1895000
   
    df_powell_water = df_powell_water.set_index("Date")
    df_powell_water = df_powell_water.sort_index()
    # print(df_powell_water)

    df_mead_water = pd.read_json(mead_data_raw)
    df_mead_water = df_mead_water.drop(df_mead_water.columns[[1,3,4,5,7,8]], axis=1)
    df_mead_water.columns = ["Site", "Water Level", "Date"]
    df_mead_water = df_mead_water[7:]
    # print(mead)
    df_mead_water['1090'] = 10857000
    df_mead_water['1075'] = 9601000
    df_mead_water['1050'] = 7683000
    df_mead_water['1025'] = 5981000
    df_mead_water['Dead Pool'] = 2547000

    df_mead_water = df_mead_water.set_index("Date")
    df_mead_water = df_mead_water.sort_index(ascending=True)
    # print(df_mead_water)
    
    # powell_df = df_powell_water.drop(df_powell_water.index[0])
    powell_df = df_powell_water
    # print(powell_df)
    mead_df = df_mead_water.drop(df_mead_water.index[0])

    start_date = date(1963, 6, 29)
    date_now = date.today()
    delta = date_now - start_date
    
    days = delta.days
    df_mead_water = mead_df[9527:]
    
    df_total = pd.merge(mead_df, powell_df, how='inner', left_index=True, right_index=True)
  
    df_total.rename(columns={'Date_x':'Date'}, inplace=True)
    
    df_total['Value_x'] = df_total['Water Level_x'].astype(int)
    df_total['Value_y'] = df_total['Water Level_y'].astype(int)
    df_total['Water Level'] = df_total['Value_x'] + df_total['Value_y']
    
    # combo_df = df_total.drop(df_total.index[0])
    combo_df = df_total
    # print(combo_df)

    return powell_df.to_json(), mead_df.to_json(), combo_df.to_json()

@app.callback(
    Output('powell-stats', 'children'),
    [Input('powell-water-data', 'data')])
def get_powell_stats(powell_data):
    powell_df = pd.read_json(powell_data)
    powell_current_volume = powell_df.iloc[-1,1]


    return html.Div([
        html.Div([
            html.Div([
                html.H6('Capacity(AF) : 24,322,000', style={'text-align': 'right'})
            ],
                className='three columns'
            ),
        ],
            className='row'
        ),
        html.Div([
            html.Div([
                html.H6('Current Volume(AF) : {:,.0f}'.format(powell_current_volume), style={'text-align': 'right'})
            ],
                className='three columns'
            ),
        ],
            className='row'
        ),
    ])

@app.callback(
    Output('powell-graph', 'figure'),
    [Input('powell-water-data', 'data'),
    Input('combo-annual-change', 'data'),
    Input('powell-year', 'value')])
def powell_graph(powell_data, powell_combo, years):
    df = pd.read_json(powell_data)
    powell_combo = pd.read_json(powell_combo)

    year1 = years[0]
    year2 = years[1]

    sel_df = df.loc[(df.index.year >= year1) & (df.index.year <= year2)]
    print(powell_combo)

   
    powell_traces = []

    powell_traces.append(go.Scatter(
        y = sel_df['Water Level'],
        x = sel_df.index,
        name='Water Level'
    )),

    powell_traces.append(go.Scatter(
        y = sel_df['power level'],
        x = sel_df.index,
        name = 'Power level'
    )),

    powell_traces.append(go.Scatter(
        y = sel_df['sick pool'],
        x = sel_df.index,
        name = 'Sick Pool'
    )),

    powell_traces.append(go.Scatter(
        y = sel_df['dead pool'],
        x = sel_df.index,
        name = 'Dead Pool'
    )),

    powell_layout = go.Layout(
        height =600,
        title = 'Lake Powell',
        yaxis = {'title':'Volume (AF)'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    return {'data': powell_traces, 'layout': powell_layout}


@app.callback([
    Output('powell-levels', 'figure'),
    Output('mead-levels', 'figure'),
    Output('combo-levels', 'figure')],
    [Input('powell-water-data', 'data'),
    Input('mead-water-data', 'data'),
    Input('combo-water-data', 'data')])
def lake_graphs(powell_data, mead_data, combo_data):
    powell_df = pd.read_json(powell_data)
    mead_df = pd.read_json(mead_data)
    combo_df = pd.read_json(combo_data)
    # print(powell_df)
    powell_traces = []
    mead_traces = []
    combo_traces = []

    data = powell_df.sort_index()
    # title = 'Lake Powell'
    powell_traces.append(go.Scatter(
        y = powell_df['Water Level'],
        x = powell_df.index,
        name='Water Level'
    )),

    for column in mead_df.columns[1:]:
        mead_traces.append(go.Scatter(
            y = mead_df[column],
            x = mead_df.index,
            name = column
        ))

    powell_traces.append(go.Scatter(
        y = powell_df['power level'],
        x = powell_df.index,
        name = 'Power level'
    )),

    powell_traces.append(go.Scatter(
        y = powell_df['sick pool'],
        x = powell_df.index,
        name = 'Sick Pool'
    )),

    powell_traces.append(go.Scatter(
        y = powell_df['dead pool'],
        x = powell_df.index,
        name = 'Dead Pool'
    )),

    combo_traces.append(go.Scatter(
        y = combo_df['Water Level'],
        x = combo_df.index,
    ))

    powell_layout = go.Layout(
        height =500,
        title = 'Lake Powell',
        yaxis = {'title':'Volume (AF)'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    mead_layout = go.Layout(
        height = 500,
        title = 'Lake Mead',
        yaxis = {'title':'Volume (AF)'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    combo_layout = go.Layout(
        height =500,
        title = 'Powell and Mead Total Storage',
        yaxis = {'title':'Volume (AF)'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )


    time.sleep(2)
    return {'data': powell_traces, 'layout': powell_layout}, {'data': mead_traces, 'layout': mead_layout}, {'data': combo_traces, 'layout': combo_layout}

@app.callback([
    Output('cur-levels', 'children'),
    Output('powell-annual-change', 'data'),
    Output('mead-annual-change', 'data'),
    Output('combo-annual-change', 'data')],
    [Input('powell-water-data', 'data'),
    Input('mead-water-data', 'data'),
    Input('combo-water-data', 'data'),
    Input('interval-component','n_intervals')])
def get_current_volumes(powell_data, mead_data, combo_data, n):
    powell_data = pd.read_json(powell_data)
    print(n)
    powell_data.sort_index()

    # print(powell_data['Water Level'].tail(20))
    powell_current_volume = powell_data.iloc[-1,1]
    powell_current_volume_date = powell_data.index[-1]
    cvd = str(powell_current_volume_date)
    powell_last_v = powell_data.iloc[-1,0]
    powell_pct = powell_current_volume / capacities['Lake Powell Glen Canyon Dam and Powerplant']
    powell_tfh_change = powell_current_volume - powell_data['Water Level'][-2]
    powell_ten = powell_current_volume - powell_data['Water Level'][-11]
    powell_cy = powell_current_volume - powell_data['Water Level'][-days]
    powell_yr = powell_current_volume - powell_data['Water Level'][-366]
    powell_last = powell_data.groupby(powell_data.index.strftime('%Y')).tail(1)
   
    # powell_last['diff'] = powell_last['Value'] - powell_last['Value'].shift(1)
    powell_last['diff'] = powell_last['Water Level'].diff()
    powell_last['color'] = np.where(powell_last['diff'] < 0, 'red', 'green')
   
    powell_annual_min = powell_data.resample('Y').min()
    powell_min_twok = powell_annual_min[(powell_annual_min.index.year > 1999)]
    powell_rec_low = powell_min_twok['Water Level'].min()
    powell_dif_rl = powell_data['Water Level'].iloc[-1] - powell_rec_low
    # powell_rec_diff = powell_current_volume - powel
    
    powell_rec_low_date = powell_data['Water Level'].idxmin().strftime('%Y-%m-%d')
    # print(powell_rec_low_date)

    mead_data = pd.read_json(mead_data)
    
    mead_data.sort_index()
    # print(mead_data['Water Level'].tail(20))
    mead_current_volume = mead_data.iloc[-0,-0]
    mead_current_volume = mead_data['Water Level'].iloc[-1]
    mead_pct = mead_current_volume / capacities['Lake Mead Hoover Dam and Powerplant']
    mead_last_v = mead_data.iloc[-1,0]
    mead_tfh_change = mead_current_volume - mead_data['Water Level'][-2]
    mead_ten = mead_current_volume - mead_data['Water Level'][-11]
    mead_cy = mead_current_volume - mead_data['Water Level'][-days]
    mead_yr = mead_current_volume - mead_data['Water Level'][-366]
    mead_last = mead_data.groupby(mead_data.index.strftime('%Y')).tail(1)
    mead_annual_min = mead_data.resample('Y').min()
    mead_min_twok = mead_annual_min[(mead_annual_min.index.year > 1999)]
    mead_rec_low = mead_min_twok['Water Level'].min()
    mead_dif_rl = mead_data['Water Level'].iloc[-1] - mead_rec_low
    
    # powell_last['diff'] = powell_last['Value'] - powell_last['Value'].shift(1)
    mead_last['diff'] = mead_last['Water Level'].diff()
    mead_last['color'] = np.where(mead_last['diff'] < 0, 'red', 'green')
    mead_rec_low_date = mead_data['Water Level'].idxmin().strftime('%Y-%m-%d')
   
    combo_data = pd.read_json(combo_data)
    
    combo_current_volume = combo_data['Water Level'][-1]
    combo_current_volume_date = combo_data.index[-1].strftime('%Y-%m-%d')
    combo_pct = combo_current_volume / capacities['Powell Mead Combo']
    combo_last_v = combo_data['Water Level'][-2]
    combo_tfh_change = combo_current_volume - combo_data['Water Level'][-2]
    combo_ten = combo_current_volume - combo_data['Water Level'][-11]
    combo_cy = combo_current_volume - combo_data['Water Level'][-days]
    combo_yr = combo_current_volume - combo_data['Water Level'][-366]
   
    combo_last = combo_data.groupby(combo_data.index.strftime('%Y')).tail(1)
    combo_last['diff'] = combo_last['Water Level'].diff()
    combo_last['color'] = np.where(combo_last['diff'] < 0, 'red', 'green')
    combo_annual_min = combo_data.resample('Y').min()
    pd.set_option('display.max_columns', None)
    # print(combo_last)
    combo_min_twok = combo_annual_min[(combo_annual_min.index.year > 1999)]
    combo_rec_low = combo_min_twok['Water Level'].min()
    combo_dif_rl = combo_data['Water Level'].iloc[-1] - combo_rec_low
    combo_rec_low_date = combo_data['Water Level'].idxmin().strftime('%Y-%m-%d')


    return html.Div([
        html.Div([
            html.Div([],className='one column'),
            html.Div([
                html.H6('Powell', style={'text-align': 'left'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(powell_current_volume), style={'text-align': 'right'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{0:.1%}'.format(powell_pct), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(powell_tfh_change), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(powell_ten), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(powell_cy), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(powell_yr), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(powell_rec_low), style={'text-align': 'right'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(powell_dif_rl), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{}'.format(powell_rec_low_date), style={'text-align': 'center'})
            ],
                className='two columns'
            ),
        ],
            className='row'
        ),
        html.Div([
            html.Div([],className='one column'),
            html.Div([
                html.H6('Mead', style={'text-align': 'left'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(mead_current_volume), style={'text-align': 'right'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{0:.1%}'.format(mead_pct), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(mead_tfh_change), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(mead_ten), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(mead_cy), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(mead_yr), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(mead_rec_low), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(mead_dif_rl), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{}'.format(mead_rec_low_date), style={'text-align': 'center'})
            ],
                className='two columns'
            ),
        ],
            className='row'
        ),
        html.Div([
            html.Div([],className='one column'),
            html.Div([
                html.H6('Combined', style={'text-align': 'left'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(combo_current_volume), style={'text-align': 'right'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{0:.1%}'.format(combo_pct), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(combo_tfh_change), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(combo_ten), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(combo_cy), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(combo_yr), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(combo_rec_low), style={'text-align': 'right'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(combo_dif_rl), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{}'.format(combo_rec_low_date), style={'text-align': 'center'})
            ],
                className='two columns'
            ),
        ],
            className='row'
        ),
        html.Div([
            html.Div([
                html.H6('Data Updated on {}'.format(combo_current_volume_date), style={'text-align': 'center'})
            ])
        ],
            className='row'
        ),
    ]), powell_last.to_json(), mead_last.to_json(), combo_last.to_json(),

@app.callback([
    Output('powell-annual-changes', 'figure'),
    Output('mead-annual-changes', 'figure'),
    Output('combo-annual-changes', 'figure')],
    [Input('powell-annual-change', 'data'),
    Input('mead-annual-change', 'data'),
    Input('combo-annual-change', 'data'),])
def change_graphs(powell_data, mead_data, combo_data):
    df_powell = pd.read_json(powell_data)
    df_powell.index = df_powell.index.year
    print(df_powell)
    df_mead = pd.read_json(mead_data)
    df_mead.index = df_mead.index.year
    df_combo = pd.read_json(combo_data)
    df_combo.index = df_combo.index.year
    pd.set_option('display.max_columns', None)
    # print(df_powell)
    # print(df_mead)
    # df_combo = df_combo.drop(df_combo.columns[[2,3,4,5]], axis=1)
    # print(df_combo)
    # df_powell['diff'] = (df_powell['diff'] !='n').astype(int)

    mead_traces = []
    powell_traces = []
    combo_traces = []

    # data = powell_traces.sort_index()

    powell_traces.append(go.Bar(
        y = df_powell['diff'],
        x = df_powell.index,
        # width = 3600000,
        marker_color = df_powell['color']
    )),

    mead_traces.append(go.Bar(
        y = df_mead['diff'],
        x = df_mead.index,
        marker_color = df_mead['color']
    )),

    combo_traces.append(go.Bar(
        y = df_combo['diff'],
        x = df_combo.index,
        marker_color = df_combo['color']
    )),

    powell_layout = go.Layout(
        height =500,
        title = 'Lake Powell',
        yaxis = {'title':'Volume (AF)'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    mead_layout = go.Layout(
        height =500,
        title = 'Lake Mead',
        yaxis = {'title':'Volume (AF)'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    combo_layout = go.Layout(
        height =500,
        title = 'Powell + Mead',
        yaxis = {'title':'Volume (AF)'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    return {'data': powell_traces, 'layout': powell_layout}, {'data': mead_traces, 'layout': mead_layout}, {'data': combo_traces, 'layout': combo_layout}

@app.callback([
    Output('blue-mesa-water-data', 'data'),
    Output('navajo-water-data', 'data'),
    Output('fg-water-data', 'data'),
    Output('ur-water-data', 'data')],
    Input('interval-component', 'n_intervals'))
def clean_powell_data(n):
    bm_df = blue_mesa_data_raw
    nav_df = navajo_data_raw
    fg_df = fg_data_raw
    # print(bm_df)

    df_bm_water = bm_df.drop(bm_df.columns[[1,3,4,5,7,8]], axis=1)
    # print(df_nav_water)
    df_bm_water.columns = ["Site", "Value", "Date"]

    df_bm_water = df_bm_water[9:]
    

    df_bm_water = df_bm_water.set_index("Date")
    df_bm_water = df_bm_water.sort_index()
    
    df_nav_water = nav_df.drop(nav_df.columns[[1,3,4,5,7,8]], axis=1)
    

    df_nav_water.columns = ["Site", "Value", "Date"]

    df_nav_water = df_nav_water[7:]
    

    df_nav_water = df_nav_water.set_index("Date")
    df_nav_water = df_nav_water.sort_index()
   
    df_fg_water = fg_df.drop(fg_df.columns[[1,3,4,5,7,8]], axis=1)
    df_fg_water.columns = ["Site", "Value", "Date"]

    df_fg_water = df_fg_water[7:]
    

    df_fg_water = df_fg_water.set_index("Date")
    df_fg_water = df_fg_water.sort_index()

    blue_mesa_df = df_bm_water.drop(df_bm_water.index[0])
    navajo_df = df_nav_water.drop(df_nav_water.index[0])
    fg_df = df_fg_water.drop(df_fg_water.index[0])

    ur_total = pd.merge(blue_mesa_df, navajo_df, how='inner', left_index=True, right_index=True)

    ur_total = pd.merge(ur_total, fg_df, how='inner', left_index=True, right_index=True)
    # print(ur_total)
    # ur_total['Water Level'] = ur_total[]

    return blue_mesa_df.to_json(), navajo_df.to_json(), fg_df.to_json(), ur_total.to_json()

@app.callback([
    Output('bm-levels', 'figure'),
    Output('navajo-levels', 'figure'),
    Output('fg-levels', 'figure')],
    [Input('blue-mesa-water-data', 'data'),
    Input('navajo-water-data', 'data'),
    Input('fg-water-data', 'data')])
def lake_graph(bm_data, nav_data, fg_data):
    bm_df = pd.read_json(bm_data)
    nav_df = pd.read_json(nav_data)
    fg_df = pd.read_json(fg_data)
    # print(fg_df)

    bm_traces = []
    nav_traces = []
    fg_traces = []

    bm_traces.append(go.Scatter(
        y = bm_df['Value'],
        x = bm_df.index,
    ))

    nav_traces.append(go.Scatter(
        y = nav_df['Value'],
        x = nav_df.index,
    ))

    fg_traces.append(go.Scatter(
        y = fg_df['Value'],
        x = fg_df.index,
    ))

    bm_layout = go.Layout(
        height =400,
        title = 'Blue Mesa Storage',
        yaxis = {'title':'Volume (AF)'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    nav_layout = go.Layout(
        height =400,
        title = 'Navajo Storage',
        yaxis = {'title':'Volume (AF)'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    fg_layout = go.Layout(
        height =400,
        title = 'Flaming Gorge Storage',
        yaxis = {'title':'Volume (AF)'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    return {'data': bm_traces, 'layout': bm_layout}, {'data': nav_traces, 'layout': nav_layout}, {'data': fg_traces, 'layout': fg_layout}

@app.callback(
    Output('upper-cur-levels', 'children'),
    [Input('blue-mesa-water-data', 'data'),
    Input('navajo-water-data', 'data'),
    Input('fg-water-data', 'data'),
    Input('ur-water-data', 'data')])
def get_current_volumes_upper(bm_data, nav_data, fg_data, ur_data):
    bm_data = pd.read_json(bm_data)
    bm_data.sort_index()
    bm_current_volume = bm_data.iloc[-1,1]
    bm_pct = bm_current_volume / capacities['BLUE MESA RESERVOIR']
    bm_tfh_change = bm_current_volume - bm_data['Value'][-2]
    bm_cy = bm_current_volume - bm_data['Value'][-days]
    bm_yr = bm_current_volume - bm_data['Value'][-366]
    bm_rec_low = bm_data['Value'].min()
    bm_dif_rl = bm_data['Value'].iloc[-1] - bm_rec_low
    bm_rec_low_date = bm_data['Value'].idxmin().strftime('%Y-%m-%d')


    nav_data = pd.read_json(nav_data)
    nav_data.sort_index()
    nav_current_volume = nav_data.iloc[-1,1]
    nav_pct = nav_current_volume / capacities['NAVAJO RESERVOIR']
    nav_tfh_change = nav_current_volume - nav_data['Value'][-2]
    nav_cy = nav_current_volume - nav_data['Value'][-days]
    nav_yr = nav_current_volume - nav_data['Value'][-366]
    nav_rec_low = nav_data['Value'].min()
    nav_dif_rl = nav_data['Value'].iloc[-1] - nav_rec_low
    nav_rec_low_date = nav_data['Value'].idxmin().strftime('%Y-%m-%d')

    fg_data = pd.read_json(fg_data)
    fg_data.sort_index()
    fg_current_volume = fg_data.iloc[-1,1]
    fg_pct = fg_current_volume / capacities['FLAMING GORGE RESERVOIR']
    fg_tfh_change = fg_current_volume - fg_data['Value'][-2]
    fg_cy = fg_current_volume - fg_data['Value'][-days]
    fg_yr = fg_current_volume - fg_data['Value'][-366]
    fg_rec_low = fg_data['Value'].min()
    fg_dif_rl = fg_data['Value'].iloc[-1] - fg_rec_low
    fg_rec_low_date = fg_data['Value'].idxmin().strftime('%Y-%m-%d')

    ur_data = pd.read_json(ur_data)
    # print(ur_data)
    ur_data['Storage'] = ur_data['Value_x'] + ur_data['Value_y'] + ur_data['Value']
    # print(ur_data)
    ur_current_volume = ur_data['Storage'].iloc[-1]
    ur_current_volume_date = ur_data.index[-1].strftime('%Y-%m-%d')
    ur_pct = ur_current_volume / capacities['UR']
    ur_tfh_change = ur_current_volume - ur_data['Storage'][-2]
    ur_cy = ur_current_volume - ur_data['Storage'][-days]
    ur_yr = ur_current_volume - ur_data['Storage'][-366]
    ur_rec_low = ur_data['Storage'].min()
    ur_dif_rl = ur_data['Storage'].iloc[-1] - ur_rec_low
    ur_rec_low_date = ur_data['Storage'].idxmin().strftime('%Y-%m-%d')
 

    return html.Div([
        html.Div([
            html.Div([],className='one column'),
            html.Div([
                html.H6('Blue Mesa', style={'text-align': 'left'})
            ],
                className = 'two columns'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(bm_current_volume), style={'text-align': 'right'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{0:.1%}'.format(bm_pct), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(bm_tfh_change), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(bm_cy), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(bm_yr), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(bm_rec_low), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(bm_dif_rl), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{}'.format(bm_rec_low_date), style={'text-align': 'center'})
            ],
                className='two columns'
            ),
        ],
            className = 'row'
        ),
        html.Div([
            html.Div([],className='one column'),
            html.Div([
                html.H6('Navajo', style={'text-align': 'left'})
            ],
                className = 'two columns'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(nav_current_volume), style={'text-align': 'right'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{0:.1%}'.format(nav_pct), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(nav_tfh_change), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(nav_cy), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(nav_yr), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(nav_rec_low), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(nav_dif_rl), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{}'.format(nav_rec_low_date), style={'text-align': 'center'})
            ],
                className='two columns'
            ),
        ],
            className = 'row'
        ),
        html.Div([
            html.Div([],className='one column'),
            html.Div([
                html.H6('Flaming Gorge', style={'text-align': 'left'})
            ],
                className = 'two columns'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(fg_current_volume), style={'text-align': 'right'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{0:.1%}'.format(fg_pct), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(fg_tfh_change), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(fg_cy), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(fg_yr), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(fg_rec_low), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(fg_dif_rl), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{}'.format(fg_rec_low_date), style={'text-align': 'center'})
            ],
                className='two columns'
            ),
        ],
            className = 'row'
        ),
        html.Div([
            html.Div([],className='one column'),
            html.Div([
                html.H6('Combined', style={'text-align': 'left'})
            ],
                className = 'two columns'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(ur_current_volume), style={'text-align': 'right'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{0:.1%}'.format(ur_pct), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(ur_tfh_change), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(ur_cy), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(ur_yr), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(ur_rec_low), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{:,.0f}'.format(ur_dif_rl), style={'text-align': 'center'})
            ],
                className='one column'
            ),
            html.Div([
                html.H6('{}'.format(ur_rec_low_date), style={'text-align': 'center'})
            ],
                className='two columns'
            ),
        ],
            className = 'row'
        ),
        html.Div([
            html.Div([
                html.H6('Data Updated on {}'.format(ur_current_volume_date), style={'text-align': 'center'})
            ])
        ],
            className='row'
        ),
    ])

@app.callback(
    Output('drought-stats', 'children'),
    [Input('combo-water-data', 'data'),
    Input('MA-input', 'value'),
    Input('drought-data', 'data'),
    Input('drought-year', 'value')])
def drought_stats(combo_data, value, drought_data, years):
    df = pd.read_json(drought_data)
    current_dsci = df['DSCI'].iloc[0]
    prev_dsci = df['DSCI'].iloc[value]

    year1 = years[0]
    year2 = years[1]
    # print(df)
    # print(years)
    selected_df = df.loc[(df.index.year >= year1) & (df.index.year <= year2)]
    # print(selected_df)
    max_dsci = selected_df.DSCI.max()
    max_dsci_date = selected_df.DSCI.idxmax().strftime('%Y-%m-%d')

    return html.Div([
        html.H6('Current DSCI = {}'.format(current_dsci)),
        html.H6('DSCI {} weeks ago = {}'.format(value, prev_dsci)),
        html.H4('Stats For {} to {}'.format(year1, year2)),
        html.H6('Max DSCI = {} on {}'.format(max_dsci, max_dsci_date))

    ])

@app.callback([
    Output('drought-graph', 'figure'),
    Output('dsci-graph', 'figure'),
    Output('diff-graph', 'figure'),],
    [Input('combo-water-data', 'data'),
    Input('drought-data', 'data'),
    Input('drought-year', 'value')])
def drought_graphs(combo_data, drought_data, years):
    year1 = years[0]
    year2 = years[1]

    df = pd.read_json(drought_data)
    selected_df = df.loc[(df.index.year >= year1) & (df.index.year <= year2)]

    drought_traces = []
    dsci_traces = []
    diff_traces = []


    df_combo = pd.read_json(combo_data)
    # print(df_combo.index.dtypes)
    selected_combo_df = df_combo.loc[(df_combo.index.year >= year1) & (df_combo.index.year <= year2)]
    selected_combo_df['color'] = np.where(selected_combo_df.index.year % 2 == 1, 'lightblue', 'aqua')
    df_combo_last = df_combo.groupby(df_combo.index.strftime('%Y')).tail(1)
    df_combo_last['diff'] = df_combo_last['Water Level'].diff()
    df_combo_last['diff'] = df_combo_last['diff'].apply(lambda x: x*-1)
    df_combo_last['Year'] = df_combo_last.index.year
    

    df_ada = df[['DSCI']]
    df_ada = df_ada.groupby(df_ada.index.strftime('%Y'))['DSCI'].mean()
  
    drought_traces.append(go.Scatter(
        name='DSCI Moving Average',
        y=selected_df['DSCI'],
        x=selected_df.index,
        marker_color = 'red',
        yaxis='y'
    )),
    drought_traces.append(go.Bar(
        name='Volume',
        y=selected_combo_df['Water Level'],
        x=selected_combo_df.index,
        yaxis='y2',
        marker_color=selected_combo_df['color']
    )),

    drought_layout = go.Layout(
        height=500,
        title='DSCI and Total Storage',
        yaxis={'title':'DSCI', 'overlaying': 'y2'},
        yaxis2={'title': 'MAF', 'side': 'right'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    dsci_traces.append(go.Scatter(
        name='Negative Vol.Change',
        y=df_combo_last['diff'],
        x=df_combo_last['Year'],
        mode='markers',
        marker_size=10,
        yaxis='y',
        marker_color='red',
        # opacity=0.5,
        # width=2
    )),

    dsci_traces.append(go.Bar(
        name='DSCI Annual Mean',
        y=df_ada,
        x=df_ada.index,
        yaxis='y2',
        marker_color='blue',
    )),

    

    dsci_layout = go.Layout(
        height= 500,
        title='Mean DSCI and Negative Volume Change',
        yaxis={'title':'MAF', 'overlaying': 'y2'},
        yaxis2={'title': 'DSCI', 'side': 'right'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    diff_layout = go.Layout(
        height = 500,
        title = 'DSCI',
        yaxis = {'title':'DSCI', 'overlaying': 'y2'},
        yaxis2 = {'title': 'MAF', 'side': 'right'},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    return {'data': drought_traces, 'layout': drought_layout}, {'data': dsci_traces, 'layout': dsci_layout}, {'data': diff_traces, 'layout': diff_layout}

@app.callback(
    Output('drought-data', 'data'),
    Input('interval-component', 'n_intervals'))
def data(n):
    url = 'https://usdmdataservices.unl.edu/api/StateStatistics/GetDroughtSeverityStatisticsByAreaPercent?aoi=08&startdate=1/1/2000&enddate=' + today + '&statisticsType=2'


    # https://usdmdataservices.unl.edu/api/StateStatistics/GetDroughtSeverityStatisticsByAreaPercent?aoi=08&startdate=1/1/2000&enddate=10/20/2021&statisticsType=2

    # combo_data = pd.read_json(com)
    # print(combo_data)
    r = requests.get(url).content

    df = pd.read_json(io.StringIO(r.decode('utf-8')))
    # print(df)

    df['date'] = pd.to_datetime(df['MapDate'].astype(str), format='%Y%m%d')

    df.drop(['StatisticFormatID', 'StateAbbreviation', 'MapDate'] , axis=1, inplace=True)
    df.set_index('date', inplace=True)
    # print(df)
    df['DSCI'] = (df['D0'] + (df['D1']*2) + (df['D2']*3) + (df['D3']*4 + (df['D4']*5)))
    # print(df)
    return df.to_json()

# #############################################################
#  DENVER TEMPS
#############################################################

@app.callback(
    [Output('all-data', 'data'),
    Output('all-temps', 'data')],
    [Input('interval-component', 'n_intervals'),
    Input('product', 'value')])
def get_temp_data(n, product):
    df = pd.read_csv('https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&dataTypes=TMAX,TMIN&stations=USW00023062&startDate=1950-01-01&endDate='+ today +'&units=standard')
    # print(df)
    df_all_temps = df
    
    df_all_temps['DATE'] = pd.to_datetime(df_all_temps['DATE'])
    df_all_temps = df_all_temps.set_index('DATE')
    # print(df_all_temps)

    return df_all_temps.to_json(), df.to_json(date_format='iso')

@app.callback(
    Output('rec-highs', 'data'),
    [Input('year', 'value'),
    Input('all-data', 'data')])
def rec_high_temps(selected_year, temp_data):
    df = pd.read_json(temp_data)
    # print(df)
    df.index = pd.to_datetime(df.index, unit='ms')
    # print(df)
    # df['DATE'] = pd.to_datetime(df['DATE'])
    # df = df.set_index('DATE')
    
    daily_highs = df.resample('D').max()
    # print(daily_highs)
    df_rec_highs = daily_highs.groupby([daily_highs['TMAX'].index.month, daily_highs['TMAX'].index.day]).max()
    # print(df_rec_highs)


    if int(selected_year) % 4 == 0:
        rec_highs = df_rec_highs
    else:
        rec_highs = df_rec_highs.drop(df_rec_highs.index[59])
    return rec_highs.to_json()

@app.callback(
    Output('rec-lows', 'data'),
    [Input('year', 'value'),
    Input('all-data', 'data')])
def rec_low_temps(selected_year, temp_data):
    df = pd.read_json(temp_data)
    # df['DATE'] = pd.to_datetime(df['DATE'])
    # df = df.set_index('DATE')
    df.index = pd.to_datetime(df.index, unit='ms')
    # print(df)
    daily_lows = df.resample('D').min()
    df_rec_lows = daily_lows.groupby([daily_lows.index.month, daily_lows.index.day]).min()

    if int(selected_year) % 4 == 0:
        rec_lows = df_rec_lows
    else:
        rec_lows = df_rec_lows.drop(df_rec_lows.index[59])
    return rec_lows.to_json()

@app.callback(
    Output('date-title', 'children'),
    Input('all-data', 'data'))
def get_temp_data(data):
    df = pd.read_json(data)
    df.index = pd.to_datetime(df.index, unit='ms')
    # print(df)

    # df['DATE'] = pd.to_datetime(df['DATE'])
    # df = df.set_index('DATE')
    last_day = df.index[-1].strftime("%Y-%m-%d")
    # print(df)
    # ld = last_day.strftime("%Y-%m-%d")

    return html.Div([
        html.H6(
            '1950-01-01 through {}'.format(last_day),
            className='twelve columns',
            style={'text-align': 'center'})
    ],
        className='row'
    ),

@app.callback(
    Output('temp-graph-layout', 'children'),
    Input('product', 'value'))
def temp_layout(product):
    # print(product)
    if product == 'temp-graph':

        layout = html.Div([
            html.H6('Select Period'),
            html.Div([
                html.Div(id='period-picker'),
                html.Div(id='year-picker'),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    dcc.Graph(id='temp-graph'),
                ],
                    className='eight columns'
                ),

                html.Div([
                    html.Div(id='graph-stats'),
                ],
                    className='four columns'
                ),
            ],
                className='row'  
            ),
        ])

        return layout

@app.callback(
    Output('climate-layout', 'children'),
    Input('product', 'value'))
def temp_layout(product):

    if product == 'climate-for-day':

        layout = html.Div([
            html.H6('Select Date'),
            html.Div([
                html.Div([
                    html.Div(id='date-picker'),
                ],
                    className='five columns'
                ),
                html.Div([
                    html.Div(id='temp-param-picker'),
                ],
                    className='seven columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div(id='climate-stuff')
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    html.Div(id='datatable-interactivity')
                ],
                    className='four columns'
                ),
                html.Div([
                    dcc.Graph(id='climate-day-bar')
                ],
                    className='eight columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div(id='daily-stats')
            ],
                className='row'
            ),
        ])

        return layout

@app.callback(
    Output('frbg-layout', 'children'),
    Input('product', 'value'))
def temp_layout(product):

    # print(product)
    if product == 'frbg':

        layout = html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(id='frs-bar')
                ],
                    className='eight columns'
                ),
                html.Div([
                    html.Div(id='frs-bar-controls')
                ],
                    className='four columns'
                ),
            ],
                className='row'
            ),
        ])

        return layout

@app.callback(
    Output('fyma-layout', 'children'),
    Input('product', 'value'))
def temp_layout(product):

    # print(product)
    if product == 'fyma-graph':

        layout = html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(id='fyma-graph')
                ],
                    className='eight columns'
                ),
                html.Div([
                    html.Div(id='fyma-param-picker')
                ],
                    className='four columns'
                ),
                html.Div([
                    html.Div(id='fyma-max-or-min-stats')
                ],
                    className='four columns'
                ),
            ],
                className='row'
            ),
        ])

        return layout

@app.callback(Output('frs-bar-controls', 'children'),
             [Input('product', 'value')])
def update_frs_graph(selected_product,):
    if selected_product == 'frbg':
        return html.Div([
            dcc.Markdown('''
            Select Max/Min and temperature to filter bar chart to show number of days 
            per year above or below selected temperature.
            '''),
            html.Div([
                html.Div(['Select Min/Max Temperature'], className='pretty_container'),
                dcc.RadioItems(
                    id='min-max-bar',
                    options=[
                        {'label':'Max', 'value':'TMAX'},
                        {'label':'Min', 'value':'TMIN'},
                    ],
                    labelStyle={'display':'inline'},
                    value='TMAX'   
                ),
                html.Div(['Select Greater/Less Than'], className='pretty_container'),
                dcc.RadioItems(
                    id='greater-less-bar',
                    options=[
                        {'label':'>=', 'value':'>='},
                        {'label':'<', 'value':'<'},
                    ],
                    labelStyle={'display':'inline'},
                    value='>='   
                ),
                html.Div(['Select Temperature'], className='pretty_container'),
                dcc.Input(
                    id='input-range',
                    type='number',
                    min=-30,
                    max=100,
                    step=5,
                    value=100
                ),
            ])
        ],
            className='round1'
        ),


@app.callback(Output('frs-bar', 'figure'),
             [Input('all-data', 'data'),
             Input('input-range', 'value'),
             Input('greater-less-bar', 'value'),
             Input('min-max-bar', 'value')])
def update_frs_graph(all_data, input_value, g_l, min_max):
    
    all_data = pd.read_json(all_data)
    all_data.index = pd.to_datetime(all_data.index, unit='ms')
    # all_data['Date'] = pd.to_datetime(all_data['Date'], unit='ms')
    # all_data.set_index(['Date'], inplace=True)
    if g_l == '>=':
        df = all_data.loc[all_data[min_max]>=input_value]
    else:
        df = all_data.loc[all_data[min_max]<input_value]
    df_count = df.resample('Y').count()[min_max]
    df = pd.DataFrame({'DATE':df_count.index, 'Selected Days':df_count.values})
    
    data = [
        go.Bar(
            y=df['Selected Days'],
            x=df['DATE'],
            marker={'color':'dodgerblue'}               
        )
    ]
    layout = go.Layout(
                xaxis={'title':'Year'},
                yaxis = {'title': '{} Degree Days'.format(input_value)},
                title ='Days Where {} is {} {} Degrees F'.format(min_max, g_l, input_value),
                paper_bgcolor="#1f2630",
                plot_bgcolor="#1f2630",
                font=dict(color="#2cfec1"),
                height = 500,
        )
    return {'data': data, 'layout': layout}

@app.callback(
    Output('fyma-graph', 'figure'),
    [Input('fyma-param', 'value'),
    Input('df5', 'data'),
    Input('max-trend', 'children'),
    Input('min-trend', 'children'),
    Input('all-data', 'data')])
def update_fyma_graph(selected_param, df_5, max_trend, min_trend, all_data):
    print(selected_param)
    fyma_temps = pd.read_json(all_data)
    fyma_temps.index = pd.to_datetime(fyma_temps.index, unit='ms')

    df_5 = pd.read_json(df_5)
    # print(df_5)
    all_max_temp_fit = pd.DataFrame(max_trend)
    print(all_max_temp_fit)
    all_max_temp_fit.index = df_5.index
    all_max_temp_fit.index = all_max_temp_fit.index.strftime("%Y-%m-%d")

    all_min_temp_fit = pd.DataFrame(min_trend)
    all_min_temp_fit.index = df_5.index
    all_min_temp_fit.index = all_min_temp_fit.index.strftime("%Y-%m-%d")

    all_max_rolling = fyma_temps['TMAX'].dropna().rolling(window=1825)
    all_max_rolling_mean = all_max_rolling.mean()
    print(all_max_rolling_mean)
    all_min_rolling = fyma_temps['TMIN'].dropna().rolling(window=1825)
    all_min_rolling_mean = all_min_rolling.mean()
    
    traces = []

    if selected_param == 'TMAX':
        traces.append(go.Scatter(
            y = all_max_rolling_mean,
            x = all_max_rolling_mean.index,
            name='Max Temp'
        )),

        traces.append(go.Scatter(
            y = all_max_temp_fit[0],
            x = all_max_temp_fit.index,
            name = 'trend',
            line = {'color':'red'}
        ))
      
    elif selected_param == 'TMIN':
        traces.append(go.Scatter(
            y = all_min_rolling_mean,
            x = all_min_rolling_mean.index,
            name='Max Temp'
        )),

        traces.append(go.Scatter(
            y = all_min_temp_fit[0],
            x = all_min_temp_fit.index,
            name = 'trend',
            line = {'color':'red'}
        ))
    
    layout = go.Layout(
        xaxis = {'rangeslider': {'visible':True},},
        yaxis = {"title": 'Temperature F'},
        title ='5 Year Rolling Mean {}'.format(selected_param),
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
        height = 500,
    )
    return {'data': traces, 'layout': layout}

@app.callback(
    Output('fyma-max-or-min-stats', 'children'),
    [Input('fyma-param', 'value'),
    Input('all-data', 'data')])
def display_fyma_stats(selected_param, all_data):
 
    fyma_temps = pd.read_json(all_data)
    fyma_temps.index = pd.to_datetime(fyma_temps.index, unit='ms')

    all_max_rolling = fyma_temps['TMAX'].dropna().rolling(window=1825)
    all_max_rolling_mean = all_max_rolling.mean()
    
    all_min_rolling = fyma_temps['TMIN'].dropna().rolling(window=1825)
    all_min_rolling_mean = all_min_rolling.mean()

    max_max = all_max_rolling_mean.max().round(2)
    max_max_index = all_max_rolling_mean.idxmax().strftime('%Y-%m-%d')
    min_max = all_max_rolling_mean.min().round(2)
    min_max_index = all_max_rolling_mean.idxmin().strftime('%Y-%m-%d')
    current_max = all_max_rolling_mean[-1].round(2)
    
    min_min = all_min_rolling_mean.min().round(2)
    min_min_index = all_min_rolling_mean.idxmin().strftime('%Y-%m-%d')
    max_min = all_min_rolling_mean.max().round(2)
    max_min_index = all_min_rolling_mean.idxmax().strftime('%Y-%m-%d')
    current_min = all_min_rolling_mean[-1].round(2)
  

    if selected_param == 'TMAX':

        return html.Div(
                [
                    html.Div([
                        html.Div('MAX STATS', style={'text-align':'center'}),
                        
                    ],
                        className='round1'
                    ),
                    html.Div([
                        html.Div('CURRENT VALUE', style={'text-align':'center'}),
                        html.Div('{}'.format(current_max), style={'text-align': 'center'})
                    ],
                        className='round1'
                    ),
                    html.Div([
                        html.Div('HIGH', style={'text-align':'center'}),
                        html.Div('{} on {}'.format(max_max, max_max_index ), style={'text-align': 'center'})
                    ],
                        className='round1'
                    ),
                    html.Div([
                        html.Div('LOW', style={'text-align':'center'}),
                        html.Div('{} on {}'.format(min_max, min_max_index ), style={'text-align': 'center'})
                    ],
                        className='round1'
                    ),
                ],
                    className='round1'
                ),
    elif selected_param == 'TMIN':

        return html.Div(
                [
                    html.Div([
                        html.Div('MIN STATS', style={'text-align':'center'}),
                    ],
                        className='round1'
                    ),
                    html.Div([
                        html.Div('CURRENT VALUE', style={'text-align':'center'}),
                        html.Div('{}'.format(current_min), style={'text-align': 'center'})
                    ],
                        className='round1'
                    ),
                    html.Div([
                        html.Div('LOW', style={'text-align':'center'}),
                        html.Div('{} on {}'.format(min_min, min_min_index ), style={'text-align': 'center'})
                    ],
                        className='round1'
                    ),
                    html.Div([
                        html.Div('HIGH', style={'text-align':'center'}),
                        html.Div('{} on {}'.format(max_min, max_min_index ), style={'text-align': 'center'})
                    ],
                        className='round1'
                    ),
                ],
                    className='round1'
                ),

@app.callback(
    Output('df5', 'data'),
    [Input('all-temps', 'data'),
    Input('product', 'value')])
def clean_df5(all_data, product_value):
    dr = pd.read_json(all_data)
    # print(dr)
    # dr.index = pd.to_datetime(dr.DATE)
    dr['DATE'] = pd.to_datetime(dr['DATE'])
    # print(dr)
    dr = dr.set_index('DATE')
    df_date_index = dr
    # print(df_date_index)
    df_ya_max = df_date_index.resample('Y').mean()
    df5 = df_ya_max[:-1]
    # print(df5)

    return df5.to_json(date_format='iso')

@app.callback(
    Output('max-trend', 'children'),
    [Input('df5', 'data'),
    Input('product', 'value')])
def all_max_trend(df_5, product_value):
    
    df5 = pd.read_json(df_5)
    # print(df5)
    # df5.index = df5.DATE
    xi = arange(0,year_count)
    slope, intercept, r_value, p_value, std_err = stats.linregress(xi,df5['TMAX'])

    return (slope*xi+intercept)

@app.callback(
    Output('min-trend', 'children'),
    [Input('df5', 'data'),
    Input('product', 'value')])
def all_min_trend(df_5, product_value):
    
    df5 = pd.read_json(df_5)
    xi = arange(0,year_count)
    slope, intercept, r_value, p_value, std_err = stats.linregress(xi,df5['TMIN'])
    
    return (slope*xi+intercept)

@app.callback(
    Output('period-picker', 'children'),
    [Input('product', 'value')])
def display_period_selector(product_value):
    # print(product_value)
    if product_value == 'temp-graph':
        return html.Div([
            dcc.RadioItems(
                id = 'period',
                options = [
                    {'label':'Annual (Jan-Dec)', 'value':'annual'},
                    {'label':'Winter (Dec-Feb)', 'value':'winter'},
                    {'label':'Spring (Mar-May)', 'value':'spring'},
                    {'label':'Summer (Jun-Aug)', 'value':'summer'},
                    {'label':'Fall (Sep-Nov)', 'value':'fall'},
                ],
                value = 'annual',
                labelStyle = {'display':'inline'}
            ),
        ])

@app.callback(
    Output('year-picker', 'children'),
    Input('product', 'value'))
def display_year_selector(product_value):

    if product_value == 'temp-graph':
        return html.Div([
            html.P('Enter Year (YYYY)') ,dcc.Input(
            id = 'year',
            type = 'number',
            value = current_year,
            min = 1950, max = current_year + 1
            )
        ])

@app.callback(
    Output('date-picker', 'children'),
    Input('product', 'value'))
    # Input('year', 'value')])
def display_date_selector(product_value):
    # print(product_value)
    # if product_value == 'climate-for-day':
    return  html.P('Select Date (MM-DD)'), dcc.DatePickerSingle(
                id='selected-date',
                display_format='MM-DD',
                date=today
            )

@app.callback(
    Output('temp-param-picker', 'children'),
    Input('product', 'value'))
    # Input('year', 'value')])
def display_date_selector(product_value):
    # print(product_value)
    # if product_value == 'climate-for-day':
    return  html.P('Select Temp. Parameter'),              dcc.RadioItems(
            id='temp-param',
            options = [
                {'label':'Max Temp', 'value':'TMAX'},
                {'label':'Min Temp', 'value':'TMIN'},
                {'label':'Temp Range', 'value':'RANGE'},
            ],
            value = 'TMAX',
                labelStyle = {'display':'inline-block'}
        )

@app.callback(
    Output('fyma-param-picker', 'children'),
    Input('product', 'value'))
    # Input('year', 'value')])
def display_fyma_param_selector(product_value):
    # print(product_value)
    # if product_value == 'climate-for-day':
    return  html.Div([
        html.P('Select Temp. Parameter'),  
        dcc.RadioItems(
            id='fyma-param',
            options = [
                {'label':'Max Temp', 'value':'TMAX'},
                {'label':'Min Temp', 'value':'TMIN'},
            ],
            # value = 'TMAX',
            labelStyle = {'display':'inline-block'}
        )
    ])
                     
            


@app.callback(
    [Output('temp-graph', 'figure'),
    Output('temps', 'data')],
    [Input('all-data', 'data'),
    Input('period', 'value'),
    Input('year', 'value'),
    Input('rec-highs', 'data'),
    Input('rec-lows', 'data')])
def temp_graph(data, period, selected_year, rec_highs,rec_lows):
    temps = pd.read_json(data)
    temps.index = pd.to_datetime(temps.index, unit='ms')
    # print(temps)
    
    df_norms = pd.read_csv('normals.csv')
    # print(df_norms)
    
    # print(period)
    previous_year = int(selected_year) - 1
    selected_year = selected_year
    # print(selected_year)

    temps['DATE'] = temps.index
    # temps = temps.set_index('DATE')
    # print(temps)
    
    last_day = temps.index[-1].strftime("%Y-%m-%d")

    temps['dif'] = temps['TMAX'] - temps['TMIN']
    # print(temps)
    temps_cy = temps[(temps.index.year==selected_year)]
    # print(temps_cy)
    temps_py = temps[(temps.index.year==previous_year)][-31:]

    df_record_highs_ly = pd.read_json(rec_highs)
    df_rh_cy = df_record_highs_ly[:len(temps_cy.index)]

    df_record_lows_ly = pd.read_json(rec_lows)
    df_rl_cy = df_record_lows_ly[:len(temps_cy.index)]
    
    

    if int(selected_year) % 4 == 0:
        df_norms = df_norms
    else:
        df_norms = df_norms.drop(df_norms.index[59])
    df_norms_cy = df_norms[:len(temps_cy.index)]
    df_norms_py = df_norms[:31]


    # rec_highs = len(temps[temps['TMAX'] == temps['rh']])
    # df_rh_cy = rec_highs[:len(temps_cy.index)]
    temps_cy.loc[:,'nh'] = df_norms_cy['DLY-TMAX-NORMAL'].values
    temps_cy.loc[:,'nl'] = df_norms_cy['DLY-TMIN-NORMAL'].values
    temps_cy.loc[:,'rl'] = df_rl_cy['TMIN'].values
    temps_cy.loc[:,'rh'] = df_rh_cy['TMAX'].values
    # print(temps)
    
    
    
    # print(df_rec_highs)
    mkr_color = {'color':'lightblue'}
  
    traces = []

    if period == 'spring':
        temps = temps_cy[temps_cy.index.month.isin([3,4,5])]
        nh_value = temps['nh']
        nl_value = temps['nl']
        rh_value = temps['rh']
        rl_value = temps['rl']
        bar_x = temps.index

    elif period == 'summer':
        temps = temps_cy[temps_cy.index.month.isin([6,7,8])]
        nh_value = temps['nh']
        nl_value = temps['nl']
        rh_value = temps['rh']
        rl_value = temps['rl']
        bar_x = temps.index

    elif period == 'fall':
        temps = temps_cy[temps_cy.index.month.isin([9,10,11])]
        nh_value = temps['nh']
        nl_value = temps['nl']
        rh_value = temps['rh']
        rl_value = temps['rl']
        bar_x = temps.index

    elif period == 'winter':
        date_range = []
        date_time = []
        sdate = date(int(previous_year), 12, 1)
        edate = date(int(selected_year), 12, 31)

        delta = edate - sdate

        for i in range(delta.days + 1):
            day = sdate + timedelta(days=i)
            date_range.append(day)
        for j in date_range:
            day = j.strftime("%Y-%m-%d")
            date_time.append(day)

        temps_py = temps_py[temps_py.index.month.isin([12])]
        temps_cy = temps_cy[temps_cy.index.month.isin([1,2])]
        temp_frames = [temps_py, temps_cy]
        temps = pd.concat(temp_frames, sort=True)
        date_time = date_time[:91]  


        df_record_highs_jan_feb = df_record_highs_ly[df_record_highs_ly.index.str.match(pat = '(1-)|(2-)')]
        df_record_highs_dec = df_record_highs_ly[df_record_highs_ly.index.str.match(pat = '(12-)')]
        high_frames = [df_record_highs_dec, df_record_highs_jan_feb]
        df_record_highs = pd.concat(high_frames)

        df_record_lows_jan_feb = df_record_lows_ly[df_record_lows_ly.index.str.match(pat = '(1-)|(2-)')]
        df_record_lows_dec = df_record_lows_ly[df_record_lows_ly.index.str.match(pat = '(12-)')]
        low_frames = [df_record_lows_dec, df_record_lows_jan_feb]
        df_record_lows = pd.concat(low_frames)

        df_high_norms_jan_feb = df_norms['DLY-TMAX-NORMAL'][0:60]
        df_high_norms_dec = df_norms['DLY-TMAX-NORMAL'][335:]
        high_norm_frames = [df_high_norms_dec, df_high_norms_jan_feb]
        df_high_norms = pd.concat(high_norm_frames)

        df_low_norms_jan_feb = df_norms['DLY-TMIN-NORMAL'][0:60]
        df_low_norms_dec = df_norms['DLY-TMIN-NORMAL'][335:]
        low_norm_frames = [df_low_norms_dec, df_low_norms_jan_feb]
        df_low_norms = pd.concat(low_norm_frames)

        bar_x = date_time
        nh_value = df_high_norms
        nl_value = df_low_norms
        rh_value = df_record_highs['TMAX']
        rl_value = df_record_lows['TMIN']

    elif period == 'annual':
        temps = temps_cy
        # annual_temps = temps_cy
    
        nh_value = temps['nh']
        nl_value = temps['nl']
        rh_value = temps['rh']
        rl_value = temps['rl']
        bar_x = temps.index
    

    traces.append(go.Bar(
        y = temps['dif'],
        x = bar_x,
        base = temps['TMIN'],
        name='Temp Range',
        marker = mkr_color,
        hovertemplate = 'Temp Range: %{y} - %{base}<extra></extra><br>'
    )),

    traces.append(go.Scatter(
        y = nh_value,
        x = bar_x,
        # hoverinfo='none',
        name='Normal High',
        marker = {'color':'indianred'}
    )),

    traces.append(go.Scatter(
        y = nl_value,
        x = bar_x,
        # hoverinfo='none',
        name='Normal Low',
        marker = {'color':'blue'}
    )),

    traces.append(go.Scatter(
        y = rh_value,
        x = bar_x,
        # hoverinfo='none',
        name='Record High',
        marker = {'color':'red'}
    )),

    traces.append(go.Scatter(
        y = rl_value,
        x = bar_x,
        # hoverinfo='none',
        name='Record Low',
        marker = {'color':'blue'}
    )),

    layout = go.Layout(
        xaxis = {'rangeslider': {'visible':False},},
        yaxis = {"title": 'Temperature F'},
        title ='{} Daily Temps'.format(selected_year),
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
        height = 500
    )

    return {'data': traces, 'layout': layout}, temps.to_json()

@app.callback(
    Output('graph-stats', 'children'),
    [Input('temps', 'data'),
    Input('product','value')])
def display_graph_stats(temps, selected_product):
    # time.sleep(1)
    temps = pd.read_json(temps)
    # print(temps)
    temps.index = pd.to_datetime(temps.index, unit='ms')
    temps = temps[np.isfinite(temps['TMAX'])]
    day_count = temps.shape[0]
    rec_highs = len(temps[temps['TMAX'] == temps['rh']])
    rec_lows = len(temps[temps['TMIN'] == temps['rl']])
    days_abv_norm = len(temps[temps['TMAX'] > temps['nh']])
    days_blw_norm = len(temps[temps['TMIN'] < temps['nl']])
    nh = temps['nh'].sum()
    nl = temps['nl'].sum()
    tmax = temps['TMAX'].sum()
    tmin = temps['TMIN'].sum()
    # nh_sum = temps['nh'][-31:].sum()
    # nh_sum2 = temps['nh'][:60].sum()

    degree_days = ((temps['TMAX'].sum() - temps['nh'].sum()) + (temps['TMIN'].sum() - temps['nl'].sum())) / 2
    if degree_days > 0:
        color = 'red'
    elif degree_days < 0:
        color = 'blue'
    if selected_product == 'temp-graph':
        return html.Div(
            [
                html.Div([
                    html.Div('Day Count', style={'text-align':'center'}),
                    html.Div('{}'.format(day_count), style={'text-align': 'center'})
                ],
                    className='round1'
                ),
                    html.Div([
                        html.Div('Records', style={'text-align':'center'}),
                        html.Div([
                            html.Div([
                                html.Div('High: {}'.format(rec_highs), style={'text-align': 'center', 'color':'red'}),
                            ],
                                className='six columns'
                            ),
                            html.Div([
                                html.Div('Low: {}'.format(rec_lows), style={'text-align': 'center', 'color':'blue'})
                            ],
                                className='six columns'
                            ),
                        ],
                            className='row'
                        ),
                    ],
                        className='round1'
                    ),
                    html.Div([
                        html.Div('Days Above/Below Normal', style={'text-align':'center'}),
                        html.Div([
                            html.Div([
                                html.Div('Above: {}'.format(days_abv_norm), style={'text-align': 'center', 'color':'red'}),
                            ],
                                className='six columns'
                            ),
                            html.Div([
                                html.Div('Below: {}'.format(days_blw_norm), style={'text-align': 'center', 'color':'blue'})
                            ],
                                className='six columns'
                            ),
                        ],
                            className='row'
                        ),
                    ],
                        className='round1'
                    ),
                    html.Div([
                        html.Div('Degree Days Over/Under Normal', style={'text-align':'center'}),
                        html.Div(html.Div('{:.0f} Degree Days'.format(degree_days), style={'text-align': 'center', 'color':color})),
                    ],
                        className='round1'
                    ),     
            ],
                className='round1'
            ),

@app.callback(
    [Output('climate-stuff', 'children'),
    Output('climate-data', 'data')],
    [Input('all-data', 'data'),
    Input('selected-date', 'date'),
    Input('product', 'value')])
def get_table_data(data, selected_date, product):
    # print(selected_date)
    dr = pd.read_json(data)
    dr.index = pd.to_datetime(dr.index, unit='ms')
    dr = dr[(dr.index.month == int(selected_date[5:7])) & (dr.index.day == int(selected_date[8:10]))]
    dr = dr.drop('STATION', axis=1)
    dr['DATE'] = pd.to_datetime(dr.index).strftime("%Y-%m-%d")
    # print(dr)
    return html.H4('Climate Data {}'.format(selected_date)), dr.to_json()

@app.callback(
    Output('daily-stats', 'children'),
    [Input('all-data', 'data'),
    Input('selected-date', 'date'),
    Input('product', 'value')])
def get_table_data(data, selected_date, product):
    # print(selected_date)
    dr = pd.read_json(data)
    dr.index = pd.to_datetime(dr.index, unit='ms')
    dr = dr[(dr.index.month == int(selected_date[5:7])) & (dr.index.day == int(selected_date[8:10]))]
    dr = dr.drop('STATION', axis=1)
    dr['DATE'] = pd.to_datetime(dr.index).strftime("%Y-%m-%d")

    d_max_max = dr['TMAX'].max()
    admaxh = dr['TMAX'].mean()
    d_min_max = dr['TMAX'].min()
    d_min_min = dr['TMIN'].min()
    adminl = dr['TMIN'].mean()
    d_max_min = dr['TMIN'].max()
    # admaxh = dr['TMAX'].mean()
    
    return html.Div([
        html.Div([
            html.Div([
                html.Div('Maximum Temperatures', style={'text-align':'center', 'color':'red'})
            ],
              className='six columns'
            ),
            html.Div([
                html.Div('Minimum Temperatures', style={'text-align':'center', 'color':'aqua'})
            ],
              className='six columns'
            ),
        ],
            className='row'
        ),
        html.Div([
            html.Div([
                html.Div([
                    html.Div('Maximum', style={'text-align':'center', 'color': 'red'}),
                    html.Div('{}'.format(d_max_max), style={'text-align':'center'})
                ],
                    className='round1 two columns'
                ),
                html.Div([
                    html.Div('Average', style={'text-align':'center', 'color': 'red'}),
                    html.Div('{:.0f}'.format(admaxh), style={'text-align':'center'})
                ],
                    className='round1 two columns'
                ),
                html.Div([
                    html.Div('Minimum', style={'text-align':'center', 'color': 'red'}),
                    html.Div('{}'.format(d_min_max), style={'text-align':'center'})
                ],
                    className='round1 two columns'
                ),
                html.Div([
                    html.Div('Maximum', style={'text-align':'center', 'color': 'blue'}),
                    html.Div('{}'.format(d_min_min), style={'text-align':'center'})
                ],
                    className='round1 two columns'
                ),
                html.Div([
                    html.Div('Average', style={'text-align':'center', 'color': 'blue'}),
                    html.Div('{:.0f}'.format(adminl), style={'text-align':'center'})
                ],
                    className='round1 two columns'
                ),
                html.Div([
                    html.Div('Minimum', style={'text-align':'center', 'color': 'blue'}),
                    html.Div('{}'.format(d_max_min), style={'text-align':'center'})
                ],
                    className='round1 two columns'
                ),
            ],
                className='pretty_container'
            ),
        ],
            className='row'
        ),
    ])

@app.callback([
    Output('datatable-interactivity', 'data'),
    Output('datatable-interactivity', 'columns')],
    [Input('climate-data', 'data'),
    Input('selected-date', 'date')])
def table_output(data, selected_date):
    dr = pd.read_json(data)
    dr.index = pd.to_datetime(dr.index, unit='ms')
    dr = dr[(dr.index.month == int(selected_date[5:7])) & (dr.index.day == int(selected_date[8:10]))]
    dr['DATE'] = pd.to_datetime(dr.index).strftime("%Y-%m-%d")
    dr = dr.fillna(0)
    # print(dr2)
    data = dr.to_dict('records')
    # print(data)
    columns=[
        {"name": i, "id": i,"selectable": False} for i in dr.columns
    ]

    return data, columns

@app.callback(
    Output('datatable-interactivity', 'children'),
    Input('selected-date', 'date'))
def display_climate_table(date):
    # print(date)
    return dt.DataTable(id='datatable-interactivity',
    data=[{}], 
    columns=[{'id': 'TMAX', 'name': 'TMAX'}, {'id': 'TMIN', 'name': 'TMIN'}, {'id': 'DATE', 'name': 'DATE'}],
    # fixed_rows={'headers': True, 'data': 0},
    style_cell_conditional=[
        {'if': {'column_id': 'DATE'},
        'width':'100px'},
        {'if': {'column_id': 'TMAX'},
        'width':'100px'},
        {'if': {'column_id': 'TMIN'},
        'width':'100px'},
    ],
    style_data_conditional=[
        {
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(248, 248, 248)'
        },
    ],
    style_header={
    'backgroundColor': 'rgb(230, 230, 230)',
    'fontWeight': 'bold'
    },
    # editable=True,
    # filter_action="native",
    sort_action="native",
    sort_mode="multi",
    column_selectable="single",
    selected_columns=[],
    selected_rows=[],
    # page_action="native",
    page_current= 0,
    page_size= 15,
    )


@app.callback(
    Output('climate-day-bar', 'figure'),
    [Input('selected-date', 'date'),
    Input('climate-data', 'data'),
    Input('temp-param', 'value'),
    Input('product', 'value')])
def climate_day_bar(selected_date, all_data, selected_param, selected_product):
    # print(selected_param)
    dr = pd.read_json(all_data)
    dr.index = pd.to_datetime(dr.index, unit='ms')
    # dr['Date'] = pd.to_datetime(dr['Date'], unit='ms')
    # dr.set_index(['Date'], inplace=True)
    dr = dr[(dr.index.month == int(selected_date[5:7])) & (dr.index.day == int(selected_date[8:10]))]
    
    dr['AMAX'] = dr['TMAX'].mean()
    dr['AMIN'] = dr['TMIN'].mean()
    # print(dr)
    xi = arange(0,len(dr['TMAX']))
    slope, intercept, r_value, p_value, std_err = stats.linregress(xi,dr['TMAX'])
    max_trend = (slope*xi+intercept)
  
    dr['MXTRND'] = max_trend
    xi = arange(0,len(dr['TMIN']))
    slope, intercept, r_value, p_value, std_err = stats.linregress(xi,dr['TMIN'])
    min_trend = (slope*xi+intercept)
    dr['MNTRND'] = min_trend
    # print(dr)
    all_max_temp_fit = pd.DataFrame(max_trend)
    all_max_temp_fit.index = dr.index
   

    all_min_temp_fit = pd.DataFrame(min_trend)
    all_min_temp_fit.index = dr.index
    
    title_param = dr.index[0].strftime('%B %d')
    # print(title_param)

    traces = []
    if selected_param == 'TMAX':
        y = dr[selected_param]
        base = 0
        color_a = 'tomato'
        color_b = 'red'
        avg_y = dr['AMAX']
        trend_y = dr['MXTRND']
        # print(trend_y)
        name = 'temp'
        name_a = 'avg high'
        name_b = 'trend'
        # hovertemplate='TMAX: %{y}'
        

    elif selected_param == 'TMIN':
        y = dr[selected_param]
        base = 0
        color_a = 'blue'
        color_b = 'dodgerblue'
        avg_y = dr['AMIN']
        trend_y = dr['MNTRND']
        name = 'temp'
        name_a = 'avg low'
        name_b = 'trend'
        # hovertemplate='TMIN: %{y}'

    else:
        y = dr['TMAX'] - dr['TMIN']
        base = dr['TMIN']
        color_a = 'dodgerblue'
        color_b = 'tomato'
        avg_y = dr['AMIN']
        trend_y = dr['AMAX']
        name = 'range'
        name_a = 'avg low'
        name_b = 'avg high'
        # hovertemplate='Temp Range: %{y} - %{base}<extra></extra><br>'

    traces.append(go.Bar(
        y=y,
        x=dr.index,
        base=base,
        marker={'color':'white'},
        name=name,
    )),

    traces.append(go.Scatter(
        y=avg_y,
        x=dr.index,
        mode = 'lines',
        name=name_a,
        line={'color': color_a},
        # hovertemplate=hovertemplate
    ))

    traces.append(go.Scatter(
        y=trend_y,
        x=dr.index,
        name=name_b,
        mode = 'lines',
        line={'color': color_b},
        # hovertemplate=hovertemplate
    ))

    layout = go.Layout(
        xaxis={'title': 'Year'},
        yaxis={'title': 'Deg F'},
        title='{} for {}'.format(selected_param,title_param),
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
        height=500
    )
    return {'data': traces, 'layout': layout} 

# @app.callback([
#     Output('datatable-interactivity', 'data'),
#     Output('datatable-interactivity', 'columns')],
#     # Output('d-max-max', 'children'),
#     # Output('avg-of-dly-highs', 'children'),
#     # Output('d-min-max', 'children'),
#     # Output('d-min-min', 'children'),
#     # Output('avg-of-dly-lows', 'children'),
#     # Output('d-max-min', 'children')],
#     [Input('all-data', 'data'),
#     Input('selected-date', 'date')])
# def display_climate_day_table(all_data, selected_date):
#     print(selected_date)
#     # if product == 'climate-for-day':
#     dr = pd.read_json(all_data)
#     print(dr)
#     dr.index = pd.to_datetime(dr.index, unit='ms')
#     # print(dr)
#     # dr['Date'] = pd.to_datetime(dr['Date'], unit='ms')
#     # dr.set_index(['Date'], inplace=True)
#     dr = dr[(dr.index.month == int(selected_date[5:7])) & (dr.index.day == int(selected_date[8:10]))]
#     # dr = dr.reset_index()
    
#     # dr.index = pd.to_datetime(dr.index, unit='ms')
#     # print(type(dr.index))

#     # print(dr)

#     dr = dr.drop('STATION', axis=1)
#     # dr["Date"] = dr.index
#     dr.index = pd.DatetimeIndex(dr.index).strftime("%Y-%m-%d")
#     # print(dr)
#     dr['DATE'] = pd.to_datetime(dr.index).strftime("%Y-%m-%d")
#     print(dr)

    # columns=[
    #     {"name": i, "id": i,"selectable": True} for i in dr.columns
    # ]

#     data = dr.to_dict('records')

    # columns=[
    # {'name': 'DATE', 'id': 'DATE', 'selectable': True},
    # {'name': 'TMAX', 'id': 'TMAX', 'selectable': True},
    # {'name': 'TMIN', 'id': 'TMIN', 'selectable': True},
    # ]

#     print(columns)
    
#     # dr['Date'] = dr.index.dt.strftime('%Y-%m-%d')
#     # dr.index = dr.index.strftime('%Y-%m-%d')
#     d_max_max = dr['TMAX'].max()
#     avg_of_dly_highs = dr['TMAX'].mean()
#     d_min_max = dr['TMAX'].min()
#     d_min_min = dr['TMIN'].min()
#     avg_of_dly_lows = dr['TMIN'].mean()
#     d_max_min = dr['TMIN'].max()

#     return data, columns

        # return dr.to_dict('records'), columns, d_max_max, avg_of_dly_highs, d_min_max, d_min_min, avg_of_dly_lows, d_max_min    

######################################################### CO2
########################################################
# @app.callback(
#     Output('co2-month-selector', 'children'),
#     Input('CO2-interval-component', 'n_intervals'))
# def co2_month(n):
#     # print(n)
#     return html.Div([
#         dcc.Dropdown(
#             id = 'CO2-month',
#             options = [
#                 {'label': 'JAN', 'value': 1},
#                 {'label': 'FEB', 'value': 2},
#                 {'label': 'MAR', 'value': 3},
#                 {'label': 'APR', 'value': 4},
#                 {'label': 'MAY', 'value': 5},
#                 {'label': 'JUN', 'value': 6},
#                 {'label': 'JUL', 'value': 7},
#                 {'label': 'AUG', 'value': 8},
#                 {'label': 'SEP', 'value': 9},
#                 {'label': 'OCT', 'value': 10},
#                 {'label': 'NOV', 'value': 11},
#                 {'label': 'DEC', 'value': 12},
#             ],
#             value = 1,
#         ),
#     ])

@app.callback(
    Output('CO2-month-data', 'data'),
    # [Input('interval-component', 'n_intervals'),
    [Input('CO2-data', 'data'),
    Input('CO2-month', 'value')])
def get_co2_month(CO2_data, CO2_month):
    
    now=datetime.now()
    today_month=now.month
    print(today_month)
    df = pd.read_json(CO2_data)
    # print(df)
    # print(type(df.index))
    # print(CO2_month)
    filtered_df = df[df.index.month == CO2_month]
    print(filtered_df)
    # min_date_allowed=date(1974, 5, 17)
    # max_date_allowed=date(today)
    # date=today
    # display_format='MMM MMMM'
    return filtered_df.to_json()

@app.callback(
    Output('CO2-data', 'data'),
    [Input('CO2-interval-component', 'n_intervals')])
def co2_graph(n):
    old_data = pd.read_csv('ftp://aftp.cmdl.noaa.gov/data/trace_gases/co2/in-situ/surface/mlo/co2_mlo_surface-insitu_1_ccgg_DailyData.txt', delim_whitespace=True, header=[150])
    print(old_data)

    old_data = old_data.drop(['hour', 'longitude', 'latitude', 'elevation', 'intake_height', 'qcflag', 'nvalue', 'altitude', 'minute', 'second', 'site_code', 'value_std_dev'], axis=1)


    old_data = old_data.iloc[501:]

    old_data.index = pd.to_datetime(old_data[['year', 'month', 'day']])
    old_data = old_data.drop(['year', 'month', 'day', 'time_decimal'], axis=1)
    print(old_data)

    new_data = pd.read_csv('https://www.esrl.noaa.gov/gmd/webdata/ccgg/trends/co2_mlo_weekly.csv')
    new_data['Date'] = pd.to_datetime(new_data['Date'])
    new_data.index = new_data['Date']
    new_data = new_data.drop(['month', 'week', 'Date'], axis=1)

    new_data['value'] = new_data['day']
    new_data = new_data.drop(['day'], axis=1)
    new_data = new_data[datetime(2021, 1, 1):]
    # print(new_data)
   
    frames = [old_data, new_data]
    co2_data = pd.concat(frames)
    co2_data['value'] = co2_data['value'].replace(-999.99, np.nan)
   
    max_co2 = co2_data['value'].max()
   
    max_co2_date = co2_data['value'].idxmax().strftime('%Y-%m-%d')
    
    current_co2 = co2_data['value'].iloc[-1]
    
    current_co2_date = co2_data.index[-1].strftime('%Y-%m-%d')
    
    monthly_avg = co2_data.groupby([co2_data.index.year, co2_data.index.month]).mean()

    current_year = datetime.now().year
    current_month = datetime.now().month
    this_month_avg = monthly_avg.loc[current_year, current_month].value
    last_year_avg = monthly_avg.loc[current_year-1, current_month].value
    print(co2_data)
    # print(co2_data.columns)
   
    return co2_data.to_json()

@app.callback(
    Output('current-co2-layout', 'children'),
    [Input('CO2-data', 'data'),
    Input('CO2-interval-component', 'n_intervals')])
def current_co2_stats(co2_data, n):
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    df = pd.read_json(co2_data)
    df['date'] = df.index.date
    # print(df)
    current_co2 = df.loc[yesterday]
    
    
    if current_co2.empty:
        current_co2 = df.loc[two_days_ago]

    current_co2_value = current_co2.iloc[-1].value
    
    current_co2_date = current_co2.iloc[-1].date
  
    return html.Div([
        html.Div([
            html.Div('Current CO2 Value (ppm)', style={'text-align':'center'}) 
        ],
            className='round1'
        ),
        html.Div([
            html.Div('{}'.format(current_co2_value), style={'text-align':'center'}),
            html.Div('{}'.format(current_co2_date), style={'text-align':'center'}) 
        ],
            className='round1'
        ),
    ])

@app.callback(
    Output('avg-co2-layout', 'children'),
    [Input('CO2-data', 'data'),
    Input('CO2-interval-component', 'n_intervals')])
def avg_co2_stats(co2_data, n):
    df = pd.read_json(co2_data)
    # print(df)
    monthly_avg = df.groupby([df.index.year, df.index.month]).mean()
    current_year = datetime.now().year
    current_month = datetime.now().month
    this_month_avg = monthly_avg.loc[current_year, current_month].value
    last_year_avg = monthly_avg.loc[current_year-1, current_month].value

    return html.Div([
        html.Div([
            html.Div('Avg For Month (ppm)', style={'text-align':'center'}),
            html.Div('{:.2f}'.format(this_month_avg), style={'text-align':'center'}), 
            html.Div('Last Year', style={'text-align':'center'}),
            html.Div('{:.2f}'.format(last_year_avg), style={'text-align':'center'}), 
        ],
            className='round1'
        ),
    ])

@app.callback(
    Output('max-co2-layout', 'children'),
    [Input('CO2-data', 'data'),
    Input('CO2-interval-component', 'n_intervals')])
def max_co2_stats(co2_data, n):
    df = pd.read_json(co2_data)
    max_co2 = df['value'].max()
    max_co2_date = df['value'].idxmax().strftime('%Y-%m-%d')

    return html.Div([
        html.Div([
            html.Div('Maximum CO2 Value (ppm)', style={'text-align':'center'}) 
        ],
            className='round1'
        ),
        html.Div([
            html.Div('{}'.format(max_co2), style={'text-align':'center'}),
            html.Div('{}'.format(max_co2_date), style={'text-align':'center'}) 
        ],
            className='round1'
        ),
    ])

@app.callback(
    Output('total-co2-stats', 'children'),
    [Input('CO2-data', 'data'),
    Input('CO2-interval-component', 'n_intervals')])
def get_monthly_co2_stats(data, n):
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

    df = pd.read_json(data)
    df['date'] = df.index.date
    current_co2 = df.loc[yesterday]
    if current_co2.empty:
        current_co2 = df.loc[two_days_ago]
    current_co2_value = current_co2.iloc[-1].value
    current_co2_date = current_co2.iloc[-1].date

    max_co2 = df['value'].max()
    max_co2_date = df['value'].idxmax().strftime('%Y-%m-%d')

    monthly_avg = df.groupby([df.index.year, df.index.month]).mean()
    current_year = datetime.now().year
    current_month = datetime.now().month
    this_month_avg = monthly_avg.loc[current_year, current_month].value
    last_year_avg = monthly_avg.loc[current_year-1, current_month].value


    return html.Div([
        html.Div([
            html.H6('Current CO2 Value (ppm)', style={'text-align':'center'}) 
        ],
            className='row'
        ),
        html.Div([
            html.H6('{} on {}'.format(current_co2_value, current_co2_date), style={'text-align':'center', 'color':'red'}),
        ],
            className='row'
        ),
        html.Div([
            html.H6('Record CO2 Value (ppm)', style={'text-align':'center'}) 
        ],
            className='row'
        ),
        html.Div([
            html.H6('{} on {}'.format(max_co2, max_co2_date), style={'text-align':'center', 'color':'red'}),
        ],
            className='row'
        ),
        html.Div([
            html.H6('Avg For Month (ppm)', style={'text-align':'center'}) 
        ],
            className='row'
        ),
        html.Div([
            html.H6('{:.2f}'.format(this_month_avg), style={'text-align':'center', 'color': 'red'}),
        ],
            className='row'
        ),
        html.Div([
            html.H6('Last Year', style={'text-align':'center'}) 
        ],
            className='row'
        ),
        html.Div([
            html.H6('{:.2f}'.format(last_year_avg), style={'text-align':'center', 'color': 'red'}),
        ],
            className='row'
        ),
    ])

@app.callback(
    Output('monthly-co2-stats', 'children'),
    [Input('CO2-month-data', 'data'),
    Input('CO2-month', 'value')])
def get_monthly_co2_stats(data, month):
    df = pd.read_json(data)

    return html.Div([
        html.Div([
            html.H2('Sup')
        ],
            className='row'
        ),
    ])

@app.callback(
    Output('monthly-co2-levels', 'figure'),
    [Input('CO2-month-data', 'data'),
    Input('CO2-month', 'value')])
def co2_month_graph(data, month):
    # print(n)
    df = pd.read_json(data)
    # df = df.groupby(df.index.year).mean()
    df_22 = df[(df.index.month == month) & (df.index.year == 2022)]
    # print(df_21)
    df_21 = df[(df.index.month == month) & (df.index.year == 2021)]

    data = [
        go.Scatter(
            y = df_22['value'],
            x = df_21.index,
            name = '2022',
            mode = 'markers',
            marker=dict(color='red'),
        ),
        go.Scatter(
            y = df_21['value'],
            x = df_21.index,
            name = '2021',
            mode = 'markers',
            marker=dict(color='blue'),
        )
    ]
    layout = go.Layout(
        title = 'Daily CO2 Measurements',
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
        yaxis=dict(
            title = 'CO2 PPM',
            showgrid = True,
            zeroline = True,
            showline = True,
            gridcolor = '#bdbdbd',
            gridwidth = 2,
            zerolinecolor = '#969696',
            zerolinewidth = 2,
            linecolor = '#636363',
            linewidth = 2,
        ),
        xaxis=dict(
            title = 'Date'
        ),
        height=500
    )

    return {'data': data, 'layout': layout}


@app.callback(
    Output('co2-levels', 'figure'),
    [Input('CO2-data', 'data'),
    Input('CO2-interval-component', 'n_intervals')])
def co2_graph(co2_data, n):
    df = pd.read_json(co2_data)

    data = [
        go.Scatter(
            y = df['value'],
            x = df.index,
            mode = 'markers',
            marker=dict(color='red'),
        )
    ]
    layout = go.Layout(
        title = 'Full CO2 Record, 1974-Present',
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
        yaxis=dict(
            title = 'CO2 PPM',
            showgrid = True,
            zeroline = True,
            showline = True,
            gridcolor = '#bdbdbd',
            gridwidth = 2,
            zerolinecolor = '#969696',
            zerolinewidth = 2,
            linecolor = '#636363',
            linewidth = 2,
        ),
        xaxis=dict(
            title = 'Date'
        ),
        height=500
    )

    return {'data': data, 'layout': layout}


#################################################
# ICE
#################################################

@app.callback([
    Output('monthly-bar', 'figure'),
    Output('df-monthly', 'data')],
    [Input('month', 'value')])
def update_figure_c(month_value):
    df_monthly = pd.read_json('https://www.ncdc.noaa.gov/snow-and-ice/extent/sea-ice/N/' + str(month_value) + '.json')
    df_monthly = df_monthly.iloc[5:]
    ice = []
    for i in range(len(df_monthly['data'])):
        ice.append(df_monthly['data'][i]['value'])
    ice = [14.42 if x == -9999 else x for x in ice]
    ice = list(map(float, ice))
    
    # trend line
    def fit():
        xi = arange(0,len(ice))
        slope, intercept, r_value, p_value, std_err = stats.linregress(xi,ice)
        return (slope*xi+intercept)

    data = [
        go.Bar(
            x=df_monthly['data'].index,
            y=ice
        ),
        go.Scatter(
                x=df_monthly['data'].index,
                y=fit(),
                name='trend',
                line = {'color':'red'}
            ),

    ]
    layout = go.Layout(
        xaxis={'title': 'Year'},
        yaxis={'title': 'Ice Extent-Million km2', 'range':[(min(ice)-1),(max(ice)+1)]},
        title='{} Avg Ice Extent'.format(month_options[int(month_value)- 1]['label']),
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )
    return {'data': data, 'layout': layout}, df_monthly.to_json()

@app.callback(
    Output('current-stats', 'children'),
    [Input('selected-sea', 'value'),
    Input('product', 'value'),
    Input('fdta', 'data')])
def update_current_stats(selected_sea, selected_product, df_fdta):
    df_fdta = pd.read_json(df_fdta)
    print(df_fdta)
    annual_max_all = df_fdta[selected_sea].loc[df_fdta.groupby(pd.Grouper(freq='Y')).idxmax().iloc[:, 0]]
    sorted_annual_max_all = annual_max_all.sort_values(axis=0, ascending=True)
    today_value = df_fdta[selected_sea][-1]
    daily_change = today_value - df_fdta[selected_sea][-2]
    week_ago_value = df_fdta[selected_sea].iloc[-7]
    weekly_change = today_value - week_ago_value
    record_min = df_fdta[selected_sea].min()
    record_min_difference = today_value - record_min
    record_low_max = sorted_annual_max_all[-1]
    record_max_difference = today_value - record_low_max
  
    if selected_product == 'years-graph':
        return html.Div([
                    html.H6('Current Extent', style={'text-align': 'center'}),
                    html.Div([
                        html.Div([
                            html.H6('{:,.0f}'.format(today_value), style={'text-align': 'center'}), 
                        ],
                            className='row'
                        ),  
                    ]),
                    html.Div([
                        html.H6('Daily Change', style={'text-align': 'center'}),
                        html.Div([
                            html.Div([
                                html.H6('{:,.0f}'.format(daily_change), style={'text-align': 'center'}), 
                            ],
                                className='row'
                            ),  
                        ]),      
                    ]),
                    html.Div([
                        html.H6('Weekly Change', style={'text-align': 'center'}),
                        html.Div([
                            html.Div([
                                html.H6('{:,.0f}'.format(weekly_change), style={'text-align': 'center'}), 
                            ],
                                className='row'
                            ),  
                        ]),      
                    ]),
                    html.Div([
                        html.H6('Diff From Rec Low Min', style={'text-align': 'center'}),
                        html.Div([
                            html.Div([
                                html.H6('{:,.0f}'.format(record_min_difference), style={'text-align': 'center'}), 
                            ],
                                className='row'
                            ),  
                        ]),      
                    ]),
                    html.Div([
                        html.H6('Diff From Rec Low Max', style={'text-align': 'center'}),
                        html.Div([
                            html.Div([
                                html.H6('{:,.0f}'.format(record_max_difference), style={'text-align': 'center'}), 
                            ],
                                className='row'
                            ),  
                        ]),      
                    ]),      
                ],
                    className='row'
                ),

@app.callback(
    Output('ice-stats', 'children'),
    [Input('product', 'value')])
def stats_n_stuff(product):
    if product == 'years-graph':
        return html.Div([
            html.Div([
                html.Div(id='year-selector')
            ],
                className='three columns'
            ), 
            html.Div([
                html.Div(id='current-stats')
            ],
                className='eight columns'
            ),
        ],
            className='twelve columns'
        ),
    elif product == 'monthly-bar':
        return html.Div([
            html.Div([
                html.Div(id='monthly-bar-stats')
            ],
                className='twelve columns'
            )
        ],
            className='twelve columns'
        ),
    elif product == 'extent-date':
        return html.Div([
            html.Div([
                html.Div([
                    html.Div(id='extent-date')
                ],
                    className='seven columns'
                ),
            ],
                className='row'
            ),
            
        ],
            className='twelve columns'
        ),
    elif product == 'moving-avg':
        return html.Div([
            html.Div([
                html.Div(id='moving-avg-stats')
            ],
                className='twelve columns'
            ),
        ],
            className='twelve columns'
        ),

@app.callback(
    Output('monthly-extent-layout', 'children'),
    Input('product', 'value'))
def monthly_extent_layout(product):
    if product == 'monthly-bar':
        return html.Div([
            html.Div([
                html.Div(id='month-selector'),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    dcc.Graph(id='monthly-bar'),
                ],
                    className='eight columns'
                ),
            ],
                className='row'
            ),
        ])

@app.callback(
    Output('ice-graph-layout', 'children'),
    Input('product', 'value'))
def ice_graph_layout(product):
    print(product)
    if product == 'years-graph':
        return html.Div([
            html.Div([
                html.Div([
                    html.Div(id='sea-selector'),
                ],
                    className='two columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    dcc.Graph(id='ice-extent'),
                ],
                    className='seven columns'
                ),
                html.Div([
                    html.Div(id='year-selector'),
                ],
                    className='one column'
                ),
                html.Div([
                    html.Div(id='ice-stats')
                ],
                    className='three columns'
                ),
            ],
                className='row'
            ),
        ])

@app.callback(
    Output('sea-selector', 'children'),
    [Input('product', 'value'),
    Input('sea-options', 'data')])
def display_sea_selector(product_value, sea_options):
    # sea_options = pd.read_json(sea_options)
    
    if product_value == 'years-graph' or product_value == 'extent-date' or product_value == 'extent-stats' or product_value == 'moving-avg':
        return html.P('Select Sea', style={'text-align': 'center'}) , html.Div([
            dcc.Dropdown(
                id='selected-sea',
                options=sea_options,
                value='Total Arctic Sea'      
            ),
        ],
            className='pretty_container'
        ),

@app.callback(
    Output('ice-data', 'data'),
    Input('ice-interval-component', 'n_intervals'))
def get_ice_data(n):
    df = pd.read_csv('ftp://sidads.colorado.edu/DATASETS/NOAA/G02186/masie_4km_allyears_extent_sqkm.csv', skiprows=1)

    # Format date and set indext to date
    df['yyyyddd'] = pd.to_datetime(df['yyyyddd'], format='%Y%j')
    df.set_index('yyyyddd', inplace=True)
    df.columns = ['Total Arctic Sea', 'Beaufort Sea', 'Chukchi Sea', 'East Siberian Sea', 'Laptev Sea', 'Kara Sea',\
        'Barents Sea', 'Greenland Sea', 'Bafin Bay Gulf of St. Lawrence', 'Canadian Archipelago', 'Hudson Bay', 'Central Arctic',\
            'Bering Sea', 'Baltic Sea', 'Sea of Okhotsk', 'Yellow Sea', 'Cook Inlet']

    return df.to_json()

@app.callback(
    Output('fdta', 'data'),
    Input('ice-data', 'data'))
def get_ice_data(data):
    df = pd.read_json(data)
    df_fdta = df.rolling(window=5).mean()

    return df.to_json()


@app.callback(
    Output('sea-options', 'data'),
    Input('ice-data', 'data'))
def get_sea_options(data):
    df = pd.read_json(data)
    sea_options = []
    for sea in df.columns.unique():
        sea_options.append({'label':sea, 'value':sea})

    return sea_options

@app.callback(
    Output('year-options', 'data'),
    Input('ice-data', 'data'))
def get_sea_options(data):
    df = pd.read_json(data)
    year_options = []
    for YEAR in df.index.year.unique():
        year_options.append({'label':(YEAR), 'value':YEAR})

    return year_options


@app.callback(
    Output('year-selector', 'children'),
    [Input('product', 'value'),
    Input('year-options', 'data')])
def display_year_selector(product_value, year_options):
    if product_value == 'years-graph':
        return html.P('Select Years') , html.Div([
                html.Div([
                dcc.Checklist(
                id='selected-years',
                options=year_options,
                value=[2012, 2021]       
                )
            ],
                className='pretty_container'
            ),
        ],
         className='twelve columns'
        ),

@app.callback(
    Output('month-selector', 'children'),
    [Input('product', 'value')])
def display_month_selector(product_value):
    if product_value == 'monthly-bar':
        return html.P('Select Month', style={'text-align': 'center'}) , html.Div([
            dcc.Dropdown(
                id='month',
                options=month_options,
                value=1     
            ),
        ],
            className='two columns'
        ),

@app.callback(
    Output('ice-extent', 'figure'),
    [Input('selected-sea', 'value'),
    Input('selected-years', 'value'),
    Input('fdta', 'data')])
def update_figure(selected_sea, selected_year, df_fdta):
    # print(selected_year)
    traces = []
    df_fdta = pd.read_json(df_fdta)
    # print(df_fdta)
    for x in selected_year:
        sorted_daily_values=df_fdta[df_fdta.index.year == x]
        traces.append(go.Scatter(
            y=sorted_daily_values[selected_sea],
            mode='lines',
            name=x
        ))
    return {
        'data': traces,
        'layout': go.Layout(
                title = '{} Ice Extent'.format(selected_sea),
                xaxis = {'title': 'Day', 'range': value_range},
                yaxis = {'title': 'Ice extent (km2)', 'showgrid': True, 'gridcolor': '#bdbdbd', 'gridwidth': 2},
                hovermode='closest',
                paper_bgcolor="#1f2630",
                plot_bgcolor="#1f2630",
                font=dict(color="#2cfec1"),
                )  
    }


#############################################################
# SNOWPACK ####################
#############################################################


@app.callback(
    Output('snow-data-raw', 'data'),
    [Input('snow-interval-component', 'n_intervals'),
    Input('river-basin', 'value')])
def get_snow_data(n, basin):
    print(n)
    
    if basin == 'state_of_colorado':
        url = 'https://www.nrcs.usda.gov/Internet/WCIS/AWS_PLOTS/basinCharts/POR/WTEQ/assocHUCco3/state_of_colorado.csv',
        df = pd.read_csv(url[0])
    else:
        url = 'https://www.nrcs.usda.gov/Internet/WCIS/AWS_PLOTS/basinCharts/POR/WTEQ/assocHUCco_8/'+ basin +'.csv',
        df = pd.read_csv(url[0])
        
    return df.to_json()

    

@app.callback(
    Output('snow-year-selector', 'children'),
    Input('snow-data-raw', 'data'))
def display_year_selector(snow_data):
    df = pd.read_json(snow_data)
    # print(df)
    df.set_index('date', inplace=True)
    columns = df.columns.values.tolist()
    # print(columns)
    snow_year_options = []
    for c in columns:
        snow_year_options.append({'label':(c), 'value':c})
    # print(snow_year_options)
    return html.Div([
        html.Div([
            dcc.Dropdown(
            id='selected-years',
            options=snow_year_options,
            multi=True,
            value=["2022", "2021", "Median ('91-'20)", "Max", "Min"]    
            )
        ],
            className='twelve columns'
        ),
    ])

@app.callback(
    [Output('snowpack-stats', 'children'),
    Output('snow-daily-pct-stats', 'children')],
    [Input('snow-data-raw', 'data'),
    Input('selected-years', 'value'),
    Input('river-basin', 'value'),
    Input('cur-mo-day', 'data'),
    Input('yes-mo-day', 'data'),
    Input('yesterday', 'data')])
def get_snow_stats(snow_data, years, basin, cur_mo_day, yes_mo_day, yesterday):
    df = pd.read_json(snow_data)
    
    df.set_index('date', inplace=True)
    pd.set_option('display.max_rows', None)
    # print(df)
    
    df_selected = df[years]
    df_selected['pct'] = df_selected['2022']/df_selected["Median ('91-'20)"]
    
    cur_data = df_selected[df_selected['2022'].notnull()]
    df_years_data = df.iloc[: , :-9]
    df_years_data = df_years_data[df_years_data['2022'].notnull()]
  
    df_cur_all_years = df_years_data.iloc[-1]
    # print(df_cur_all_years)
    sorted_cur_all_years = df_cur_all_years.sort_values()
   
    today_rank = sorted_cur_all_years.index.get_loc('2022')+1
    total_years = len(sorted_cur_all_years)
   
    today_snow = cur_data.iloc[-1]
  
    yest_snow = cur_data.iloc[-2]
    today = cur_data.index[-1]

    pon = today_snow['2022'] / today_snow["Median ('91-'20)"]
    # print(pon)
    ypon = yest_snow['2022'] / yest_snow["Median ('91-'20)"]
    day_change = pon - ypon
    # print(day_change)
    lypon = today_snow['2021'] / today_snow["Median ('91-'20)"]
    year_change = pon - lypon


    return html.Div([
        html.Div([
            html.H6('Updated {}'.format(today),style={'text-align': 'center'}),
            html.H6('% of Median : {0:.1%}'.format(pon),style={'text-align': 'left'}),
            html.H6('24-hr change : {0:.1%}'.format(day_change),style={'text-align': 'left'}),
            html.H6('1 Year Change : {0:.1%}'.format(year_change),style={'text-align': 'left'})
        ],
            className='row'
        ),
    ]), html.Div([
        html.H6('Current SWE : {:,.1f}'.format(today_snow['2022'])),
        html.H6('Rank(low to high) : {} of {}'.format(today_rank, total_years)),
        html.H6('Normal SWE : {:,.1f}'.format(today_snow["Median ('91-'20)"])),
        html.H6('Max SWE : {:,.1f}'.format(today_snow["Max"])),
        html.H6('Min SWE : {:,.1f}'.format(today_snow["Min"])),
    ])



@app.callback(
    [Output('snow-graph', 'figure'),
    Output('snow-daily-pct', 'figure')],
    [Input('snow-data-raw', 'data'),
    Input('selected-years', 'value'),
    Input('river-basin', 'value')])
def get_snow_graph(snow_data, years, basin):
    df = pd.read_json(snow_data)
    
    df.set_index('date', inplace=True)
    df['pct'] = df['2022']/df["Median ('91-'20)"]
    # print(df)
    pd.set_option('display.max_rows', None)
    df1 = df[years]
    df1.columns = [years]
    # print(df1)
    # df1['pct'] = df1['2022']/df1["Median ('91-'20)"]
    df_pct = df[['2022', 'pct']].copy()
    # df_pct = df_pct.drop(df_pct[df_pct.index < '11-01'].index)
    # df_pct = df_pct.drop(df_pct[df_pct.index < '10-01'].index)
    # print(df)
    df_pct = df.iloc[30: , :]
    print(df_pct)
    # print(df1)
    df_median = df[["Median ('91-'20)"]]
    
    data = []

    color_list = ['white', 'blue', 'goldenrod', 'green', 'red', 'pink']

    for idx, col in enumerate(df1.columns):
        for x in col:
            data.append(go.Scatter(
                y=df1[col],
                x=df1.index,
                name=x,
                line_color=color_list[idx]
            ))

    layout = go.Layout(
        title = '{} Snowpack Data'.format(basin.capitalize()),
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
        yaxis=dict(
            title = 'SWE',
            showgrid = True,
            zeroline = True,
            showline = True,
            gridcolor = '#bdbdbd',
            gridwidth = 1,
            zerolinecolor = '#969696',
            zerolinewidth = 2,
            linecolor = '#636363',
            linewidth = 2,
        ),
        xaxis=dict(
            type = 'category',
            title = 'Date',
            tickformat = '%m-%d',
            tickvals = ['10-01', '12-01', '02-01', '04-01', '06-01', '08-01', '09-30'],
            showgrid = True,
            gridcolor = '#bdbdbd',
            gridwidth = .5,
        ),
        height=500
    )

    data2 = [
        go.Scatter(
            y = df_pct['pct'],
            x = df_pct.index,
            mode = 'lines',
            marker=dict(color='red'),
        )
    ]

    layout2 = go.Layout(
        title = 'Snowpack as Pct. of Normal',
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
        yaxis=dict(
            title = 'Pct of Normal',
            showgrid = True,
            zeroline = True,
            showline = True,
            gridcolor = '#bdbdbd',
            gridwidth = 1,
            zerolinecolor = '#969696',
            zerolinewidth = 2,
            linecolor = '#636363',
            linewidth = 2,
        ),
        xaxis=dict(
            type = 'category',
            title = 'Date',
            tickformat = '%m-%d',
            tickvals = ['10-01', '11-01', '12-01', '01-01', '02-01', '03-01', '04-01', '05-01', '06-01'],
            showgrid = True,
            gridcolor = '#bdbdbd',
            gridwidth = .5,
        ),
        height=500
    )


    return {'data': data, 'layout': layout}, {'data': data2, 'layout': layout2}





if __name__ == '__main__':
    app.run_server(debug=True)