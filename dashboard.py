import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output
import pandas as pd

# dataset and so on
df = pd.read_csv('Invistico_Airline.csv')
cats = ['Gender', 'Customer Type', 'Type of Travel', 'Class']
rating = ['Seat comfort', 'Departure/Arrival time convenient', 'Food and drink', ' Gate location',
          'Inflight wifi service', 'Inflight entertainment', 'Online support', 'Ease of Online booking',
          'On-board service', 'Leg room service', 'Baggage handling', 'Checkin service', 'Cleanliness',
          'Online boarding']
nums = ['Age', 'Flight Distance', 'Departure Delay in Minutes', 'Arrival Delay in Minutes']
target = 'satisfaction'


# You can guess this func output
def sunBurstComponents():
    return html.Div(
        [
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.P(
                                "Overall Distribution",
                                style={
                                    'text-align': 'center',
                                    'font-size': 20,
                                    'margin-bottom': 5
                                }
                            ),

                            dcc.RadioItems(
                                options=[
                                    {'label': ' Satisfied\t', 'value': 1},
                                    {'label': ' Dissatisfied   ', 'value': 2}
                                ],
                                value=1,
                                id='sunburst_select',
                                style={
                                    'text-align': 'center',
                                }
                            ),
                            dcc.Graph(
                                id='sunburst_graph'
                            )
                        ]
                    )
                ]
            ),
        ]
    )


# for numerical data
def numComponents():
    return html.Div(
        [
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dcc.Dropdown(
                                id='select_num',
                                options=[{"label": f"{i}", "value": i} for i in nums],
                                multi=False,
                                value=None,
                                style={'font-size': 12}
                            ),
                            dcc.Graph(
                                id='num_graph',
                            )
                        ]
                    )
                ]
            ),
        ]
    )


# for categorical data
def catComponents():
    return html.Div(
        [
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dcc.Dropdown(
                                id='select_cat',
                                options=[{"label": f"{i}", "value": i} for i in rating + cats],
                                multi=False,
                                value=None,
                                style={'font-size': 12}
                            ),
                            dcc.Graph(
                                id='cat_graph',
                            )
                        ]
                    )
                ]
            ),
        ]
    )


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
app.name = 'Dashboard'
app.layout = dbc.Container(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Div(
                                        [

                                            html.P('Invistico Airline', style={
                                                'text-align': 'center',
                                                'font-size': 40,
                                                'margin-top': 0,
                                                'margin-bottom': 0,
                                                'color': 'white'
                                            }
                                                   ),
                                            html.P('Performance Dashboard', style={
                                                'text-align': 'center',
                                                'font-size': 20,
                                                'margin-top': 0,
                                                'margin-bottom': 0,
                                                'color': 'white'
                                            }
                                                   )
                                        ], style={
                                            'margin-top': 0,
                                            'margin-bottom': 20
                                        }
                                    ),
                                    sunBurstComponents()
                                ], width=4, style={
                                    'margin-top': 10,
                                    'margin-bottom': 0
                                }
                            ),
                            dbc.Col(
                                [
                                    dbc.Row(
                                        [
                                            numComponents()
                                        ]
                                    ),
                                    dbc.Row(
                                        [
                                            catComponents()
                                        ]
                                    )
                                ], width=10, lg=8, style={
                                    'text-align': 'center',
                                    'margin-top': 0,
                                    'margin-bottom': 0
                                }
                            )
                        ]
                    )
                ]
            )
        ),
    ], style={'margin': dict(t=0, l=0, r=0, b=0)}
)


# func to update num_graph value
@app.callback(Output(component_id='num_graph', component_property='figure'),
              [Input(component_id='select_num', component_property='value')])
def update_num(option):
    df_copy = df.copy()
    if (not option):
        option = 'Age'
    if (option in nums):
        fig_num = px.histogram(df_copy, x=option, color=target, width=680, height=230)
    return fig_num.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(t=0, l=0, r=0, b=0)
    )


# func to update cat_graph value
@app.callback(Output(component_id='cat_graph', component_property='figure'),
              [Input(component_id='select_cat', component_property='value')])
def update_cat(option):
    df_copy = df.copy()
    if (not option):
        option = 'Gender'
    if (option in cats) | (option in rating):
        df_copy = df_copy.groupby([target, option]).size().reset_index()
        df_copy.columns = [target, option, 'count']
        fig_cat = px.bar(df_copy, x=option, y='count', color=target, barmode='stack', width=680, height=230)
    return fig_cat.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(t=0, l=0, r=0, b=0)
    )


# func to update sunburst_graph
@app.callback(Output(component_id='sunburst_graph', component_property='figure'),
              [Input(component_id='sunburst_select', component_property='value')])
def update_sunburst(option):
    df_copy = df.copy()

    if option == 1:
        df_copy[target] = df_copy[target].map({'satisfied': 1, 'dissatisfied': 0})
        fig_sun = px.sunburst(
            df_copy[df_copy[target] == 1],
            path=['Gender', 'Customer Type', 'Type of Travel', 'Class'],
            values='satisfaction',
            width=300,
            height=300
        )
    elif option == 2:
        df_copy[target] = df_copy[target].map({'satisfied': 0, 'dissatisfied': 1})
        df_copy['dissatisfied'] = df_copy[target]
        fig_sun = px.sunburst(
            df_copy[df_copy['dissatisfied'] == 1],
            path=['Gender', 'Customer Type', 'Type of Travel', 'Class'],
            values='dissatisfied',
            width=300,
            height=300
        )
    return fig_sun.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(t=0, l=0, r=0, b=0)
    )


# main func
if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
