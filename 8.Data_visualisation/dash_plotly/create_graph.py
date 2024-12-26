import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import io,requests

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
            options=[{'label': str(year), 'value': year} for year in df['Date'].str[:4].unique()],
            value=df['Date'].str[:4].iloc[0]  # Default value
        )
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
    
    # Graphs for Recession Report Statistics
    html.Div([
        # Line chart for Average Automobile Sales Fluctuation Over Recession Period (Year-wise)
        dcc.Graph(id='avg-sales-fluctuation'),
        
        # Bar chart for Average Number of Vehicles Sold by Vehicle Type
        dcc.Graph(id='avg-vehicles-by-type'),
        
        # Pie chart for Total Expenditure Share by Vehicle Type During Recessions
        dcc.Graph(id='expenditure-share'),
        
        # Bar chart for Effect of Unemployment Rate on Vehicle Type and Sales
        dcc.Graph(id='unemployment-effect')
    ], style={'margin-top': '20px'})
])

# Define callback functions to update graphs based on the selected year
@app.callback(
    [Output('avg-sales-fluctuation', 'figure'),
     Output('avg-vehicles-by-type', 'figure'),
     Output('expenditure-share', 'figure'),
     Output('unemployment-effect', 'figure')],
    [Input('year-dropdown', 'value')]
)
def update_graphs(year):
    # Filter data based on the selected year
    filtered_df = df[df['Date'].str[:4] == year]
    
    # Average Automobile Sales Fluctuation Over Recession Period (Year-wise)
    avg_sales = filtered_df.groupby('Date')['Automobile_Sales'].mean().reset_index()
    sales_fluctuation_fig = {
        'data': [go.Scatter(x=avg_sales['Date'], y=avg_sales['Automobile_Sales'], mode='lines', name='Sales')],
        'layout': go.Layout(title='Average Automobile Sales Fluctuation Over Recession Period (Year-wise)', xaxis={'title': 'Year'}, yaxis={'title': 'Average Sales'})
    }
    
    # Average Number of Vehicles Sold by Vehicle Type
    avg_vehicles = filtered_df.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
    avg_vehicles_fig = {
        'data': [go.Bar(x=avg_vehicles['Vehicle_Type'], y=avg_vehicles['Automobile_Sales'], name='Average Sales')],
        'layout': go.Layout(title='Average Number of Vehicles Sold by Vehicle Type', xaxis={'title': 'Vehicle Type'}, yaxis={'title': 'Average Sales'})
    }
    
    # Total Expenditure Share by Vehicle Type During Recessions
    expenditure_share = filtered_df.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
    expenditure_share_fig = {
        'data': [go.Pie(labels=expenditure_share['Vehicle_Type'], values=expenditure_share['Advertising_Expenditure'])],
        'layout': go.Layout(title='Total Expenditure Share by Vehicle Type During Recessions')
    }
    
    # Effect of Unemployment Rate on Vehicle Type and Sales
    unemployment_effect = filtered_df.groupby('Vehicle_Type')['Unemployment_Rate', 'Automobile_Sales'].mean().reset_index()
    unemployment_effect_fig = {
        'data': [
            go.Bar(x=unemployment_effect['Vehicle_Type'], y=unemployment_effect['Unemployment_Rate'], name='Unemployment Rate', yaxis='y1'),
            go.Bar(x=unemployment_effect['Vehicle_Type'], y=unemployment_effect['Automobile_Sales'], name='Sales', yaxis='y2')
        ],
        'layout': go.Layout(
            title='Effect of Unemployment Rate on Vehicle Type and Sales',
            xaxis={'title': 'Vehicle Type'},
            yaxis=dict(title='Unemployment Rate', side='left'),
            yaxis2=dict(title='Sales', overlaying='y', side='right')
        )
    }
    
    return sales_fluctuation_fig, avg_vehicles_fig, expenditure_share_fig, unemployment_effect_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
