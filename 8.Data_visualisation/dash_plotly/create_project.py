import dash
import dash_core_components as dcc
import dash_html_components as html

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1('XYZAutomotives: Historical Trends in Automobile Sales Analysis'),
    html.Div([
        html.P('This dashboard provides insights into how XYZAutomotives\' sales were impacted during recession periods.')
    ])
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
