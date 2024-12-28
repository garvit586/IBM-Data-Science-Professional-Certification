import dash
import dash_core_components as dcc
import dash_html_components as html

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(
            "Automobile Sales Statistics Dashboard",
            style={
                "textAlign": "center",  # Center align the text
                "color": "black",      # Text color
                "fontSize": "36px",    # Font size
                "marginTop": "20px",   # Add some margin
            },
        ),
    html.Div([
        html.P('This dashboard provides insights into how XYZAutomotives\' sales were impacted during recession periods.')
    ])
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
