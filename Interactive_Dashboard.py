# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)

							    dcc.Dropdown(id='site-dropdown', 
								options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
									{'label': 'CCAFS LC-40', 'value': 'OPT1'},
									{'label': 'VAFB SLC-4E', 'value': 'OPT2'},
                                    {'label': 'KSC LC-39A', 'value': 'OPT3'},
                                    {'label': 'CCAFS SLC-40', 'value': 'OPT4'}
								],
                                value='ALL',
								placeholder='Select a Launch Site here',
                                searchable=True),
								#style={'width':'80%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'}),                                



                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    marks={
                                        0: '0',
                                        2500: '2500',
                                        5000: '5000',
                                        7500: '7500',
                                        10000: '10000'
                                    },
                                    value=[min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))

def get_graph(chart):
    
    if chart == 'ALL':
        pie_data = spacex_df.groupby(['Launch Site'])['class'].sum().reset_index()
        pie_fig = px.pie(pie_data, values='class', names='Launch Site', title='Total Success Launches By Site')
    elif chart == 'OPT1':
        pie_data = spacex_df.loc[spacex_df['Launch Site']=='CCAFS LC-40']
        pie_data = pie_data.groupby(['Launch Site'])['class'].value_counts()
        pie_fig = px.pie(pie_data, values='class', names='class', title='Total Success Launches of Site CCAFS LC-40')
   
    elif chart == 'OPT2':
        pie_data = spacex_df.loc[spacex_df['Launch Site']=='VAFB SLC-4E']
        pie_data = pie_data.groupby(['Launch Site'])['class'].value_counts()
        pie_fig = px.pie(pie_data, values='class', names='class', title='Total Success Launches of Site VAFB SLC-4E')

    elif chart == 'OPT3':
        pie_data = spacex_df.loc[spacex_df['Launch Site']=='KSC LC-39A']
        pie_data = pie_data.groupby(['Launch Site'])['class'].value_counts()
        pie_fig = px.pie(pie_data, values='class', names='class', title='Total Success Launches of Site KSC LC-39A')

    elif chart == 'OPT4':
        pie_data = spacex_df.loc[spacex_df['Launch Site']=='CCAFS SLC-40']
        pie_data = pie_data.groupby(['Launch Site'])['class'].value_counts()
        pie_fig = px.pie(pie_data, values='class', names='class', title='Total Success Launches of Site CCAFS SLC-40')
    

    return pie_fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


@app.callback(  Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value')])

def get_graph(chart, slider_range):
    
    if chart == 'ALL':
        low, high = slider_range
        mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
        sca_fig = px.scatter(spacex_df[mask], x="Payload Mass (kg)", y="class", color="Booster Version Category", title='Correlation between Payload and Success for all Sites')
    
    elif chart == 'OPT1':
        low, high = slider_range
        sca_data = spacex_df.loc[spacex_df['Launch Site']=='CCAFS LC-40']
        mask = (sca_data['Payload Mass (kg)'] > low) & (sca_data['Payload Mass (kg)'] < high)
        sca_fig = px.scatter(sca_data[mask], x="Payload Mass (kg)", y="class", color="Booster Version Category", title='Correlation between Payload and Success for CCAFS LC-40')

    elif chart == 'OPT2':
        low, high = slider_range
        sca_data = spacex_df.loc[spacex_df['Launch Site']=='VAFB SLC-4E']
        mask = (sca_data['Payload Mass (kg)'] > low) & (sca_data['Payload Mass (kg)'] < high)
        sca_fig = px.scatter(sca_data[mask], x="Payload Mass (kg)", y="class", color="Booster Version Category", title='Correlation between Payload and Success for VAFB SLC-4E')

    elif chart == 'OPT3':
        low, high = slider_range
        sca_data = spacex_df.loc[spacex_df['Launch Site']=='KSC LC-39A']
        mask = (sca_data['Payload Mass (kg)'] > low) & (sca_data['Payload Mass (kg)'] < high)
        sca_fig = px.scatter(sca_data[mask], x="Payload Mass (kg)", y="class", color="Booster Version Category", title='Correlation between Payload and Success for KSC LC-39A')

    elif chart == 'OPT4':
        low, high = slider_range
        sca_data = spacex_df.loc[spacex_df['Launch Site']=='CCAFS SLC-40']
        mask = (sca_data['Payload Mass (kg)'] > low) & (sca_data['Payload Mass (kg)'] < high)
        sca_fig = px.scatter(sca_data[mask], x="Payload Mass (kg)", y="class", color="Booster Version Category", title='Correlation between Payload and Success for CCAFS SLC-40')


        #sca_fig = px.scatter(spacex_df, x="Payload Mass (kg)", y="class", color="Booster Version Category")

    return sca_fig



# Run the app
if __name__ == '__main__':
    app.run_server()
