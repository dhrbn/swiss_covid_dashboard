
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
            ]),
            dbc.Button(
                "Reset",
                color='primary',
                id='reset_button',
            ),
        ]),
        html.Hr(),
        dbc.Row([
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(
                        id='swiss_map_figure',
                        figure=controller.get_swiss_map_figure(),
                        config=dict(displayModeBar=False, scrollZoom=False),
                    ),
                ]),
            ),
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H3("Covid cases evolution", className="card-title"),
                        dcc.Graph(
                            id='cases_evolution_figure',
                            figure=controller.get_cases_evolution_figure(),
                            style={'height': '200px'},
                        ),
                    ]),
                ),
                dbc.Card(
                    dbc.CardBody([
                        html.H3("Deaths and hospitalizations evolution", className="card-title"),
                        dcc.Graph(
                            id='hosps_evolution_figure',
                            figure=controller.get_hosps_evolution_figure(),
                            style={'height': '200px'},
                        ),
                    ]),
                ),
            ]),
        ]),
        dbc.Row([
            dbc.Card(
                dbc.CardBody([
                    html.H3("Vaccination coverage", className="card-title"),
                    dcc.Graph(
                        id='vaccination_coverage_figure',
                        figure=controller.get_vaccination_coverage_figure(),
                        style={'height': '350px', 'width': '350px'},
                    ),
                ]),
            ),
            dbc.Card(
                dbc.CardBody([
                    html.H3("Vaccine types", className="card-title"),
                    dcc.Graph(
                        id='vaccines_figure',
                        figure=controller.get_vaccines_figure(),
                        style={'height': '350px', 'width': '350px'},
                    ),
                ]),
            ),
            dbc.Card(
                dbc.CardBody([
                    html.H3("Current cases age repartition", className="card-title"),
                    dcc.Graph(
                        id='age_repartition_figure',
                        figure=controller.get_age_repartition_figure(),
                        style={'height': '350px', 'width': '350px'},
                    ),
                ]),
            ),
            dbc.Card(
                dbc.CardBody([
                    html.H3("Total count data", className="card-title"),

                    dcc.Graph(
                        id='total_count_figure',
                        figure=controller.get_total_count_figure(),
                        style={'height': '250px', 'width': '550px'},
                    ),
                    html.H4(f"Deaths per cases ratio: 1 for {controller.get_deaths_cases_ratio()}",
                            id='deaths_per_cases_ratio', style={'font-size': '2.5em', 'padding-top': '20px'}),
                    html.H4(f"Deaths per hospitalizations ratio: 1 for {controller.get_deaths_hospitalizations_ratio()}",
                            id='deaths_per_hospitalizations_ratio', style={'font-size': '2.5em'}),
                ]),
            ),
        ]),
    ], style={'max-width': '100%', 'max-height': '100%'})
])


@app.callback(
    [
        Output('cases_evolution_figure', 'figure'),
        Output('hosps_evolution_figure', 'figure'),
        Output('vaccination_coverage_figure', 'figure'),
        Output('vaccines_figure', 'figure'),
        Output('age_repartition_figure', 'figure'),
        Output('swiss_map_figure', 'figure'),
        Output('total_count_figure', 'figure'),
        Output('deaths_per_cases_ratio', 'children'),
        Output('deaths_per_hospitalizations_ratio', 'children'),
    ],
    [
        Input('swiss_map_figure', 'clickData'),
        Input('reset_button', 'n_clicks'),
    ]
)
def region_update(click_data, button_clicked):
    if button_clicked is not None and button_clicked > controller.get_reset_clicks():
        region = 'CH'
        controller.set_reset_clicks(button_clicked)
    elif click_data is not None and click_data['points'][0]['location'] != controller.get_current_region():
        region = click_data['points'][0]['location']
    else:
        region = 'CH'

    controller.set_current_region(region)

    return [
        controller.get_cases_evolution_figure(),
        controller.get_hosps_evolution_figure(),
        controller.get_vaccination_coverage_figure(),
        controller.get_vaccines_figure(),
        controller.get_age_repartition_figure(),
        controller.get_swiss_map_figure(),
        controller.get_total_count_figure(),
        f"Deaths per cases ratio: 1 for {controller.get_deaths_cases_ratio()}",
        f"Deaths per hospitalizations ratio: 1 for {controller.get_deaths_hospitalizations_ratio()}",
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
