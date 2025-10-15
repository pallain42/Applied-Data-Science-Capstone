import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Data
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# App
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] +
                [{'label': s, 'value': s} for s in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder='Select a Launch Site',
        searchable=True
    ),
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P('Payload range (Kg):'),
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload, max=max_payload, step=1000,
        value=[min_payload, max_payload]
    ),
    html.Br(),
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# Callbacks
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value'))
def update_pie(site):
    if site == 'ALL':
        fig = px.pie(spacex_df, names='Launch Site', values='class',
                     title='Total Success Launches by Site')
    else:
        df = spacex_df[spacex_df['Launch Site'] == site]
        fig = px.pie(df, names='class', title=f'Success vs Failure for {site}')
    return fig

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')])
def update_scatter(site, payload_range):
    lo, hi = payload_range
    df = spacex_df[(spacex_df['Payload Mass (kg)'] >= lo) &
                   (spacex_df['Payload Mass (kg)'] <= hi)]
    if site != 'ALL':
        df = df[df['Launch Site'] == site]
    fig = px.scatter(df, x='Payload Mass (kg)', y='class',
                     color='Booster Version Category',
                     title='Payload vs. Outcome')
    return fig

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8050)
