from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd
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
app = Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("Dynamic Report and Graph Display"),
    
    # Dropdown for selecting report type
    html.Div([
        html.Label("Select Report Type:"),
        dcc.Dropdown(
            id='report-dropdown',
            options=[
                {'label': 'Sales Report', 'value': 'sales'},
                {'label': 'Consumer Confidence', 'value': 'confidence'}
            ],
            value='sales'
        )
    ], style={'margin-bottom': '20px'}),
    
    # Input container
    html.Div(id='input-container', style={'margin-bottom': '20px'}),
    
    # Output container for graphs
    dcc.Graph(id='output-container')
])

# Callback 1: Update the input-container based on report type
@app.callback(
    Output('input-container', 'children'),
    Input('report-dropdown', 'value')
)
def update_input_container(report_type):
    if report_type == 'sales':
        return html.Div([
            html.Label("Enter Sales Date Range:"),
            dcc.DatePickerRange(
                id='sales-date-range',
                start_date=df['Date'].min(),
                end_date=df['Date'].max()
            )
        ])
    elif report_type == 'confidence':
        return html.Div([
            html.Label("Enter Consumer Confidence Threshold:"),
            dcc.Input(
                id='confidence-threshold',
                type='number',
                placeholder='Enter threshold value'
            )
        ])

# Callback 2: Update the output-container based on user input
@app.callback(
    Output('output-container', 'figure'),
    [Input('report-dropdown', 'value'),
     Input('sales-date-range', 'start_date'),
     Input('sales-date-range', 'end_date'),
     Input('confidence-threshold', 'value')]
)
def update_output_container(report_type, start_date, end_date, confidence_threshold):
    if report_type == 'sales' and start_date and end_date:
        filtered_data = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        figure = {
            'data': [go.Bar(x=filtered_data['Date'], y=filtered_data['Sales'], name='Sales')],
            'layout': go.Layout(title='Sales Report', xaxis={'title': 'Date'}, yaxis={'title': 'Sales'})
        }
        return figure
    elif report_type == 'confidence' and confidence_threshold is not None:
        filtered_data = df[df['Confidence'] >= confidence_threshold]
        figure = {
            'data': [go.Scatter(x=filtered_data['Date'], y=filtered_data['Confidence'], mode='lines', name='Confidence')],
            'layout': go.Layout(title='Consumer Confidence Report', xaxis={'title': 'Date'}, yaxis={'title': 'Confidence Index'})
        }
        return figure
    return {}

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
