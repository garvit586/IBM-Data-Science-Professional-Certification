import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import requests
import io

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
    
    # Placeholder for output (for future graphs or data)
    html.Div(id='output-container')
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
