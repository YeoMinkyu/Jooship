import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

fs = pd.read_csv(
    '/Users/mk/Documents/Financial/Financial_Statements/SBUX_from_Numbers.csv',
    error_bad_lines=False
)


def select_fs():
    # information_rows = ['Revenue USD Mil', 'Operating Income USD Mil', 'Operating Margin %', 'Net Income USD Mil', 'Net Margin %']
    # fs_reformed = reform_fs()
    # information_df = fs_reformed.loc['Revenue USD Mil']
    information_rows = [2, 4, 5, 6, 7, 8, 9, 12, 14, 32, 43, 48]
    information_df = fs.iloc[information_rows]
    new_columns = np.append(np.array(['Year']), fs.iloc[1, 1:].values)
    information_df.columns = new_columns

    return information_df


def generate_table(data_frame):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in data_frame.columns])] +

        # Body
        [html.Tr([
            html.Td(data_frame.iloc[i][col]) for col in data_frame.columns
        ]) for i in range(min(len(data_frame), data_frame.shape[0]))]
    )


def visualize_table(dash_app):
    information_df = select_fs()
    dash_app.layout = html.Div(children=[
        html.H4(children='StarBucks Financial Statements'),
        generate_table(information_df)
    ])


def visualize_graph(dash_app):
    information_df = select_fs()
    chart_columns = information_df.columns.values[1:]

    dash_app.layout = html.Div(children=[
        html.H4(children='StarBucks Financial Statements'),
        generate_table(information_df),

        html.H2(children='Visualization'),

        html.Div(children='''
            Chart Analysis
        '''),

        dcc.Graph(
            id='r-o-n-graph',
            figure={
                'data': [
                    {'x': chart_columns, 'y': information_df.values[0, 1:], 'type': 'bar', 'name': 'Revenue USD'},
                    {'x': chart_columns, 'y': information_df.values[1, 1:], 'type': 'bar', 'name': 'Operating Income'},
                    {'x': chart_columns, 'y': information_df.values[3, 1:], 'type': 'bar', 'name': 'Net Income'},

                ],
                'layout':[
                    {'title': 'Dash Data Visualization', 'yAxis': {'title': 'USD'}}
                ]
             }
        ),

        dcc.Graph(
            id='margin-graph',
            figure={
                'data': [
                    {'x': chart_columns, 'y': information_df.values[2, 1:], 'type': 'graph',
                     'name': 'Operating Margin %'},
                    {'x': chart_columns, 'y': information_df.values[9, 1:], 'type': 'graph',
                     'name': 'Net Margin %'}
                ],
                'layout':[
                    {'title': 'Margin Data Visualization'}
                ]
            }
        ),

        dcc.Graph(
            id='cash-flow-graph',
            figure={
                'data': [
                    {'x': chart_columns, 'y': information_df.values[7, 1:], 'type': 'bar',
                     'name': 'Operating Cash Flow USD'},
                    {'x': chart_columns, 'y': information_df.values[8, 1:], 'type': 'bar',
                     'name': 'Free Cash Flow USD'}
                ],
                'layout': [
                    {'title': 'Cash Flow Data Visualization'}
                ]
            }
        ),

        dcc.Graph(
            id='EPS-graph',
            figure={
                'data': [
                    {'x': chart_columns, 'y': information_df.values[4, 1:], 'type': 'bar',
                     'name': 'Earning Per Share USD'},
                ],
                'layout': [
                    {'title': 'EPS Data Visualization'}
                ]
            }
        ),

        dcc.Graph(
            id='YoY-graph',
            figure={
                'data': [
                    {'x': chart_columns, 'y': information_df.values[10, 1:], 'type': 'graph',
                     'name': 'Revenue YoY %'},
                    {'x': chart_columns, 'y': information_df.values[11, 1:], 'type': 'graph',
                     'name': 'Operating Income YoY %'}
                ],
                'layout': [
                    {'title': 'YoY Data Visualization'}
                ]
            }
        ),

        dcc.Graph(
            id='dividends-graph',
            figure={
                'data': [
                    {'x': chart_columns, 'y': information_df.values[5, 1:], 'type': 'bar',
                     'name': 'Dividends USD'},
                ],
                'layout': [
                    {'title': 'Dividends Data Visualization'}
                ]
            }
        ),

        dcc.Graph(
            id='payout-ratio-graph',
            figure={
                'data': [
                    {'x': chart_columns, 'y': information_df.values[6, 1:], 'type': 'graph',
                     'name': 'Payout Ratio %'},
                ],
                'layout': [
                    {'title': 'Payout Ratio Data Visualization'}
                ]
            }
        )

    ])


if __name__ == '__main__':
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    # reform_fs()
    visualize_graph(app)
    # visualize_table(app)
    app.run_server(debug=True)