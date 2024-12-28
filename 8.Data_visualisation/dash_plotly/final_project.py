import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import io, requests

# URL of the CSV file
URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"

# Fetch the data from the URL
response = requests.get(URL)
response.raise_for_status()  # Raise an error if the request fails
csv_content = io.StringIO(response.text)

# Read the CSV data into a pandas dataframe
df = pd.read_csv(csv_content)

# Ensure correct data types and extract the year from the date
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1('Automobile Sales Statistics Dashboard'),
    
    # Dropdown for Year Selection
    html.Div([
        html.Label('Select Year:'),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': year} for year in df['Year'].unique()],
            value=df['Year'].min()  # Default value
        )
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),

    # Graphs for Yearly Report Statistics
    html.Div([
        dcc.Graph(id='avg-sales-fluctuation'),  # Line chart
        dcc.Graph(id='avg-vehicles-by-type'),  # Bar chart
        dcc.Graph(id='expenditure-share'),  # Pie chart
        dcc.Graph(id='unemployment-effect')  # Dual-axis bar chart
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
    filtered_df = df[df['Year'] == year]
    
    # Average Automobile Sales Fluctuation Over the Year
    avg_sales = filtered_df.groupby(filtered_df['Date'].dt.month)['Automobile_Sales'].mean().reset_index()
    avg_sales_fluctuation_fig = {
        'data': [go.Scatter(x=avg_sales['Date'], y=avg_sales['Automobile_Sales'], mode='lines', name='Sales')],
        'layout': go.Layout(title=f'Average Automobile Sales Fluctuation - {year}', 
                            xaxis={'title': 'Month'}, yaxis={'title': 'Average Sales'})
    }
    
    # Average Number of Vehicles Sold by Vehicle Type
    avg_vehicles = filtered_df.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
    avg_vehicles_fig = {
        'data': [go.Bar(x=avg_vehicles['Vehicle_Type'], y=avg_vehicles['Automobile_Sales'], name='Average Sales')],
        'layout': go.Layout(title=f'Average Vehicles Sold by Type - {year}', 
                            xaxis={'title': 'Vehicle Type'}, yaxis={'title': 'Average Sales'})
    }
    
    # Total Expenditure Share by Vehicle Type
    expenditure_share = filtered_df.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
    expenditure_share_fig = {
        'data': [go.Pie(labels=expenditure_share['Vehicle_Type'], values=expenditure_share['Advertising_Expenditure'])],
        'layout': go.Layout(title=f'Total Advertising Expenditure Share by Type - {year}')
    }
    
    # Effect of Unemployment Rate on Vehicle Type and Sales
    unemployment_effect = filtered_df.groupby('Vehicle_Type')[['unemployment_rate', 'Automobile_Sales']].mean().reset_index()
    unemployment_effect_fig = {
        'data': [
            go.Bar(x=unemployment_effect['Vehicle_Type'], y=unemployment_effect['unemployment_rate'], name='Unemployment Rate'),
            go.Bar(x=unemployment_effect['Vehicle_Type'], y=unemployment_effect['Automobile_Sales'], name='Sales')
        ],
        'layout': go.Layout(
            title=f'Effect of Unemployment on Sales - {year}',
            xaxis={'title': 'Vehicle Type'},
            yaxis={'title': 'Unemployment Rate', 'side': 'left'},
        )
    }
    
    return avg_sales_fluctuation_fig, avg_vehicles_fig, expenditure_share_fig, unemployment_effect_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
