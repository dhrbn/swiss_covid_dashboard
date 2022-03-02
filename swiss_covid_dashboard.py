
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from controller import Controller
from display_utils import MAIN_COLOR, MIDDLE_GRAY

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css',
    'https://use.fontawesome.com/releases/v5.7.2/css/all.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True

controller = Controller()


app.layout = html.Div([
    html.Div(className='container', children=[
        dbc.Row([
            dbc.Col([
                html.H1(f"Swiss Covid Dashboard", style={'color': MAIN_COLOR})
            ], )
        ]),
        html.Hr(),
        # html.Div(id='useless_div', style={'display': 'none'}),

        dbc.Row([
            html.H3(f"Region:", style={'color': MIDDLE_GRAY}),
            dcc.Dropdown(
                id='regions_dropdown',
                options=[{'label': i, 'value': i} for i in controller.get_regions()],
                value=controller.get_regions()[0],
                clearable=False
            ),
        ]),
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    id='cases_evolution_figure',
                    figure=controller.get_cases_evolution_figure(),
                ),
            ])
        ),
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    id='hosps_evolution_figure',
                    figure=controller.get_hosps_evolution_figure(),
                ),
            ])
        ),
    # ], style={'max-width': '3000px'})
    ])
])


@app.callback(
    Output('cases_evolution_figure', 'figure'),
    [
        Input('regions_dropdown', 'value'),
    ]
)
def mmi_update(region):
    controller.set_current_region(region)
    return controller.get_cases_evolution_figure()


if __name__ == '__main__':
    app.run_server(debug=True)
