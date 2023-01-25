# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 08:13:40 2023

@author: khadim
"""

import dash
from dash import Dash, dcc, html, Input, Output , dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import geopandas as gpd
import pandas as pd
from datetime import datetime
from modules.geo import geoM
from modules.graph import Graph

df = pd.read_csv('modules/data/meatadata_2.tsv', sep = '\t')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

#--------------------table

# table = dbc.Table.from_dataframe(df,striped=True, bordered=True,dark=True, hover=True,responsive=True,style={'text-align': 'center'})
def table(d_df):
    table = dash_table.DataTable(
                id='datatable_id',
                data=d_df.to_dict('records'),
                columns=[
                    {"name": i, "id": i, "deletable": False, "selectable": False} for i in df.columns
                ],
                editable=False,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                row_selectable="multi",
                row_deletable=False,
                selected_rows=[],
                page_action="native",
                page_current= 0,
                page_size= 50,
                # page_action='none',
                # style_cell={
                # 'whiteSpace': 'normal'
                # },
                # fixed_rows={ 'headers': True, 'data': 0 },
                # virtualization=False,
                style_cell_conditional=[
                    {'if': {'column_id': 'countriesAndTerritories'},
                     'width': '40%', 'textAlign': 'left'},
                    {'if': {'column_id': 'deaths'},
                     'width': '30%', 'textAlign': 'left'},
                    {'if': {'column_id': 'cases'},
                     'width': '30%', 'textAlign': 'center'},
                ],
                style_data_conditional=[
                    {
                        'backgroundColor': '#FFFFFF',
                        'color': '#000000',
                        'textAlign': 'center',
                        'font-size': '20px'
                    }]
            )
    return table
#----------------------tabs

tabs = dbc.Tabs(
    [
        dbc.Tab(label="Table",tab_id = 'tab_table'),
        dbc.Tab( label="Graph",tab_id = 'tab_graph'),
        dbc.Tab( label="Map",tab_id = 'tap_map')
    ],
    id="tabs",
    active_tab="tab_table",
    style={'font-size': '30px'}
)

#-------------------------country dropdown ,  WHO, lineage
country_dropdown= dcc.Dropdown( [str(i) for i in df['country'].unique()],
                     [''],id ='country_dropdown',
                     multi=True, style = {'font-size': '25px'})
who_dropdown= dcc.Dropdown(id ='who_dropdown',multi=True, style = {'font-size': '25px'})
lineage_dropdown= dcc.Dropdown(id ='lineage_dropdown',multi=True, style = {'font-size': '25px'})
color_by = dcc.RadioItems(id='radion_button',options =['Continent', 'Country', 'Lineage','WHO'], value =  'Country' ,inline=False,style = {'font-size': '25px','width' : '35%'})



#---------------------------------main app
# html.Img(src="/assets/images/language_icons/julia_50px.svg", height=30),
# bottom_card = dbc.Card([
#         dbc.CardBody(html.P("This has a bottom image", className="card-text")),
#         dbc.CardImg(src="/static/images/placeholder286x180.png", bottom=True),
#     ],
#     style={"width": "18rem"},
#     )

app.layout = html.Div([
    html.Div([
        dbc.Row(
            [
                dbc.Col([
                    html.A(html.Img(src="https://www.ebi.ac.uk/web_guidelines/images/logos/ena/ENA-logo.png"), href = 'https://www.ebi.ac.uk/ena/browser/home') 
                    ]),
                dbc.Col([
                    html.Div('Dashboard')
                    ])
                ])
        
       
        
        ]
             ,style={'font-size': '80px' ,'font-weight': 'bold', 'font-family': 'Helvetica, Arial, sans-serif', 'width' : '100%','background-color': '#40E0D0','text-align': 'center'}),
    html.Hr(),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col([
                        html.Div("Menu",style={'font-size': '50px','text-align':'center','font-weight': 'bold'}),
                        html.Hr(),
                        dcc.Markdown('* Country',style = {'font-size': '25px'}),
                        country_dropdown,
                        html.Br(),
                        dcc.Markdown('* WHO',style = {'font-size': '25px'}),
                        who_dropdown,
                        html.Br(),
                        dcc.Markdown('* Lineages',style = {'font-size': '25px'}),
                        lineage_dropdown,
                        html.Br(),
                        html.Hr(),
                        dcc.Markdown('* Color Map by',style = {'font-size': '25px'}),
                        color_by,
                        
                             
                    ]
                    , width=3,style={'background-color': '#808080'}),
                    dbc.Col(html.Div([
                        tabs,
                        html.Hr(),
                        html.Div(id = 'tab_content')
                        # table
                    
                    ]), width=9),
                ] 
            )
        ],style={'margin-left':'1%', 'margin-right':'1%'})
    
    ])

#-------------Map
def map (nv_data,color):
    if color=='Continent':
        c = 'ContinentName'
    elif color == 'Country':
        c = 'CountryName'
    elif color == 'Lineage':
        c = 'lineage'
    else :
        c = 'who'
    MG = geoM()
    fig= MG.map(nv_data,c)
    
    return html.Div(dcc.Graph(figure=fig)) #height: 100px

#----------------------------graph 
def graph(nv_data):
    Gh_1 = Graph()
    fig1 = Gh_1.pie(nv_data,'country')
    fig2 = Gh_1.pie(nv_data,'lineage')
    fig3 = Gh_1.pie(nv_data,'who')
    res = html.Div([
        dbc.Row(
            [
                dbc.Col([
                    html.Div('Distribution of samples by country',style = {'font-size': '20px','font-weight': 'bold','text-align':'center'}),
                    dcc.Graph(figure=fig1)
                    ],width=6),
                dbc.Col([
                    html.Div('Distribution of samples by Lineage',style = {'font-size': '20px','font-weight': 'bold','text-align':'center'}),
                    dcc.Graph(figure=fig2)
                    ],width=6)
                
            ]),
        dbc.Row(
            [
                dbc.Col([
                    html.Div('Distribution of samples by WHO labels',style = {'font-size': '20px','font-weight': 'bold','text-align':'center'}),
                    dcc.Graph(figure=fig3)
                    ],width=6),
                
            ]),
        
        ],style={'margin-left':'1%', 'margin-right':'1%','width':'100%'})
    return res

#---------------------tabs callback
@app.callback(Output("tab_content", "children"),
               Output("who_dropdown", "options")
               ,Output("lineage_dropdown", "options"),
              [Input("tabs", "active_tab"),
               Input(component_id='country_dropdown', component_property='value'),
               Input(component_id='who_dropdown', component_property='value'),
               Input(component_id='lineage_dropdown', component_property='value'),
               Input(component_id='radion_button', component_property='value')
               ]
              )
def switch_tab(at,country_input,who_input,lineage_input,color):
    if who_input is None : 
        who_input = []
    if lineage_input is None : 
        lineage_input = []
    current_dateTime = datetime.now()
    print('\033[92m'+'[ '+str(current_dateTime)+' ] Action ...')
    print('\033[0m')
    new_df,v,l = update_df(country_input,who_input,lineage_input)
    if at == "tab_table":
        return table(new_df),v,l
    elif at == "tab_graph":
        return graph(new_df),v,l
    elif at == 'tap_map':
        return map(new_df,color) , v, l
    return html.P("This shouldn't ever be displayed...")


def update_df(country_input,who_input,lineage_input):
    # print (country_input)
    # return df
    if len(country_input) == 0: 
        country_input.append('')
    if len(who_input) == 0 :
        who_input.append('')
    if len(lineage_input) == 0:
        lineage_input.append('')
    if (country_input[0] == '')  and ( who_input[0] == '')  and (lineage_input[0] =='' ):
        v = [str(i) for i in df['who'].unique()]
        l = [str(i) for i in df['lineage'].unique()]
        return df,v,l
    else :
        new_df = df[df['country'].isin(country_input) | df['who'].isin(who_input) | df['lineage'].isin(lineage_input)]
        v = [str(i) for i in new_df['who'].unique()]
        l = [str(i) for i in new_df['lineage'].unique()]
        return new_df,v,l

    

if __name__=='__main__':
    app.run_server(debug=True, use_reloader=False, port=8050) # use_reloader=False