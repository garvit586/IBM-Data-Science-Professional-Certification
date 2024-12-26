import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import requests, io

# URL of the CSV file
URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"

# Fetch the data from the URL
response = requests.get(URL)

# Raise an error if the request failed
response.raise_for_status()

# Convert the response content into a readable format for pandas
csv_content = io.StringIO(response.text)

# Read the CSV data into a pandas dataframe
df = pd.read_csv(csv_content)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1('XYZAutomotives: Historical Trends in Automobile Sales Analysis'),
    
    # Dropdown for Year Selection
    html.Div([
        html.Label('Select Year:'),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': year} for year in df['Year'].unique()],
            value=df['Year'].iloc[0]  # Default value
        )
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
    
    # Dropdown for Vehicle Type Selection
    html.Div([
        html.Label('Select Vehicle Type:'),
        dcc.Dropdown(
            id='vehicle-dropdown',
            options=[{'label': vehicle, 'value': vehicle} for vehicle in df['Vehicle_Type'].unique()],
            value=df['Vehicle_Type'].iloc[0]  # Default value
        )
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
    
    # Output division for displaying the results
    html.Div(id='output-container', className='output-container', children=[
        html.H3("Output will be displayed here based on selections."),
        # You can later replace this content with dynamic output like graphs or data
    ], style={'padding': '20px', 'border': '1px solid #ccc', 'margin-top': '20px'})
])

# Define callback function to update the output based on dropdown selections
@app.callback(
    Output('output-container', 'children'),
    [Input('year-dropdown', 'value'),
     Input('vehicle-dropdown', 'value')]
)
def update_output(year, vehicle_type):
    # Replace with dynamic output, such as charts or other content based on selections
    return html.Div([
        html.H4(f'Selected Year: {year}'),
        html.H4(f'Selected Vehicle Type: {vehicle_type}')
    ])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
