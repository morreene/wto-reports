import os

"""
This app creates a responsive sidebar layout with dash-bootstrap-components and
some custom css with media queries.

When the screen is small, the sidebar moved to the top of the page, and the
links get hidden in a collapse element. We use a callback to toggle the
collapse when on a small screen, and the custom CSS to hide the toggle, and
force the collapse to stay open when the screen is large.

dcc.Location is used to track the current location. There are two callbacks,
one uses the current location to render the appropriate page content, the other
uses the current location to toggle the "active" properties of the navigation
links.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_table

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
# df = pd.read_csv('data-tpr-20191003.zip', compression='zip')
# df = pd.read_csv('gapminder2007.csv')
df = pd.read_csv('tpr-data-20191011.csv')
# cat_list = list(df['Cat'].unique())
cat_list = ['economic environment',
 'investment regime',
 'customs procedures',
 'customs valuation',
 'rules of origin',
 'mfn tariff',
 'preferential tariffs',
 'import prohibitions, restrictions, and licensing',
 'anti-dumping',
 'safeguard',
 'standards and other technical requirements',
 'taxes, charges, and levies',
 'export prohibitions',
 'export subsidies',
 'export finance, insurance, and guarantees',
 'incentives',
 'competition policy and price controls',
 'government procurement',
 'intellectual property',
 'agriculture',
 'manufacturing',
 'services',
 'wto',
 'import prohibition',
 'sanitary and phytosanitary',
 'competition',
 'energy',
 'trade policy objectives',
 'trade agreements and arrangements',
 'bound',
 'agricultural',
 'state trading',
 'fisheries',
 'general framework',
 'tariff exemptions',
 'internal taxes',
 'legal framework',
 'other charges affecting imports',
 'mining and energy',
 'tariff bindings',
 'countervailing',
 'investment policy',
 'legal and institutional framework',
 'preferential agreements',
 'agriculture, forestry, and fisheries',
 'anti-dumping, countervailing, and safeguard measures',
 'export support and promotion',
 'registration, customs procedures and requirements',
 'other measures affecting imports'
  '',
]
country_list = ['','747#BWA#LSO#NAM#ZAF', '808', 'AGO', 'ALB', 'ARE', 'ARG', 'ARM', 'ATG#DMA#GRD#KNA#LCA#VCT', 'AUS', 'BDI#KEN#RWA#TZA#UGA', 'BEN#BFA#CIV#GNB#MLI#NER#SEN#TGO', 'BGD', 'BHR', 'BLZ', 'BOL', 'BRA', 'BRB', 'BRN', 'CAF#CMR#COG#GAB#TCD', 'CAN', 'CHE#LIE', 'CHL', 'CHN', 'COD', 'COL', 'CPV', 'CRI', 'DJI', 'DOM', 'EEC', 'EGY', 'FJI', 'GEO', 'GHA', 'GIN', 'GMB', 'GTM', 'GUY', 'HKG', 'HND', 'HTI', 'IDN', 'IND', 'ISL', 'ISR', 'JAM', 'JOR', 'JPN', 'KGZ', 'KHM', 'KOR', 'LKA', 'MAC', 'MAR', 'MDA', 'MDG', 'MDV', 'MEX', 'MMR', 'MNE', 'MNG', 'MOZ', 'MRT', 'MUS', 'MWI', 'MYS', 'NGA', 'NIC', 'NOR', 'NPL', 'NZL', 'OMN', 'PAK', 'PAN', 'PER', 'PHL', 'PRY', 'QAT', 'RUS', 'SAU', 'SGP', 'SLB', 'SLE', 'SLV', 'SUR', 'THA', 'TON', 'TPKM', 'TUN', 'TUR', 'UKR', 'URY', 'USA', 'VNM', 'VUT', 'ZMB']

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']
# with "__name__" local css under assets is also included
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

server = app.server
app.config.suppress_callback_exceptions = True
# we use the Row and Col components to construct the sidebar header
# it consists of a title, and a toggle, the latter is hidden on large screens
sidebar_header = dbc.Row(
    [
        dbc.Col(html.H2("Reports", className="display-4000")),
        dbc.Col(
            html.Button(
                # use the Bootstrap navbar-toggler classes to style the toggle
                html.Span(className="navbar-toggler-icon"),
                className="navbar-toggler",
                # the navbar-toggler classes don't set color, so we do it here
                style={
                    "color": "rgba(0,0,0,.5)",
                    "bordercolor": "rgba(0,0,0,.1)",
                },
                id="toggle",
            ),
            # the column containing the toggle will be only as wide as the
            # toggle, resulting in the toggle being right aligned
            width="auto",
            # vertically align the toggle in the center
            align="center",
        ),
    ]
)

sidebar = html.Div(
    [
        sidebar_header,
        # we wrap the horizontal rule and short blurb in a div that can be
        # hidden on a small screen
        html.Div(
            [
                html.Hr(),
                html.P(
                    "Select a topic or country ",
                    className="lead",
                ),
            ],
            id="blurb",
        ),
        # use the Collapse component to animate hiding / revealing links
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink("TPR Reports", href="/page-1", id="page-1-link"),
                    dbc.NavLink("Charts", href="/page-2", id="page-2-link"),
                    dbc.NavLink("Help", href="/page-3", id="page-3-link"),
                ],
                vertical=True,
                pills=True,
            ),
            id="collapse",
        ),
    ],
    id="sidebar",
)

content = html.Div(id="page-content")

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 4)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return html.Div([
            dbc.Row(
                [
                    dbc.Col([
                        html.H5('Topic'),
                        dcc.Dropdown(
                            id='dropdown_1',
                            # options=[{'label': i, 'value': i} for i in ['Select','China', 'Argentina', 'Belgium']],
                            options=[{'label': i, 'value': i} for i in cat_list],
                            # multi=True,
                            value='economic environment'
                        ),
                    ], width=6, align="center"),
                    dbc.Col(
                        [
                        html.H5('Country'),
                        dcc.Dropdown(
                            id='dropdown_2',
                            options=[{'label': i, 'value': i} for i in country_list],
                            value=''
                        ),
                        ], width=6
                    ),
                ],
            ),
            html.Br(),
            html.Div(id='table-container')
        ])

    elif pathname == "/page-2":
        return html.P("This is the content of page 2. Yay!")
    elif pathname == "/page-3":
        return html.P("Oh cool, this is page 3!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

# Page 1 dropdown control
@app.callback(
    dash.dependencies.Output('table-container', 'children'),
    [dash.dependencies.Input('dropdown_1', 'value'),
     dash.dependencies.Input('dropdown_2', 'value')
    ])
def display_table(dropdown_value_1, dropdown_value_2):
    # dff = df
    # if dropdown_value_1 == 'Select':
    #     dff = df
    # dff = df[(df['Cat'].str.contains(dropdown_value_1)) &
    #         (df['ConcernedCountriesCode'].str.contains(dropdown_value_2))]
    # dff = df[(df['Cat'].str.contains(dropdown_value_1))]
    dff = df[(df['Cat'].str.contains(dropdown_value_1)) &
            (df['Country'].str.contains(dropdown_value_2))]
    return html.Div([
            dash_table.DataTable(
                    id='tab',
                    columns=[
                        {"name": i, "id": i, "deletable": False, "selectable": False} for i in dff.columns
                    ],
                    data = dff.to_dict('records'),
                    editable=False,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    column_selectable=False,
                    row_selectable=False,
                    row_deletable=False,
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current= 0,
                    page_size= 20,
    #                     style_data={
    #     'whiteSpace': 'normal',
    #     'height': 'auto'
    # },
        style_cell={
        'height': 'auto',
        'minWidth': '50px', 'maxWidth': '180px',
        'whiteSpace': 'normal'
    },
                    # style_cell_conditional=[
                    #         {'if': {'column_id': 'Text'},
                    #          'width': '50%', 'height': 'auto'},
                    #          ],
    # style_cell={
    #     'height': 'auto',
    #     'minWidth': '0px', 'maxWidth': '180px',
    #     'whiteSpace': 'normal'
    # }
                )
            ])




@app.callback(
    Output("collapse", "is_open"),
    [Input("toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True)
