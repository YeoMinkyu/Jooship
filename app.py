import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import copy

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

file_name = '/Users/mk/Documents/Financial/Financial_Statements/MMM_from_Numbers.csv'

fs = pd.read_csv(
    file_name,
    error_bad_lines=False
)


def select_fs():
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


def _make_head_title():
    _file_name = copy.deepcopy(file_name)
    _title = _file_name.split('/')[-1]
    _title = _title.split('_')[0]
    _title = _title + " Financial Statements"
    return _title


def visualize_graph(dash_app):
    information_df = select_fs()
    chart_columns = information_df.columns.values[1:]
    _head_title = _make_head_title()

    dash_app.layout = html.Div(children=[
        html.H4(children=_head_title),
        generate_table(information_df),

        html.H2(children='Visualization'),

        html.Div(children='''
            Chart Analysis
        '''),

        dcc.Graph(
            id='r-o-n-multiple-axis',
            figure={
                'data': [go.Bar(x=chart_columns, y= information_df.values[0, 1:], name= 'Revenue USD'),
                         go.Bar(x=chart_columns, y= information_df.values[1, 1:], name= 'Operating Income'),
                         go.Bar(x=chart_columns, y=information_df.values[3, 1:], name='Net Income'),
                         go.Scatter(x=chart_columns, y=information_df.values[2, 1:], name='Operating Margin %', yaxis='y2'),
                         go.Scatter(x=chart_columns, y=information_df.values[9, 1:], name='Operating Margin %',
                                    yaxis='y2')
                         ],

                'layout': go.Layout(
                            xaxis={'title': 'Year'},
                            yaxis={'title': 'USD'},
                            yaxis2={'title': 'Percent %', 'overlaying': 'y', 'side': 'right'}
                )
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
            id='EPS-YoY-graph',
            figure={
                'data': [go.Bar(x=chart_columns, y=information_df.values[4, 1:], name='Earning Per Share USD'),
                         go.Scatter(x=chart_columns, y=information_df.values[10, 1:], name='Revenue YoY %',
                                    yaxis='y2'),
                         go.Scatter(x=chart_columns, y=information_df.values[11, 1:], name='Operating Income YoY %',
                                    yaxis='y2')
                         ],
                'layout': go.Layout(
                    xaxis={'title': 'Year'},
                    yaxis={'title': 'EPS USD'},
                    yaxis2={'title': 'YoY %', 'overlaying': 'y', 'side': 'right'}
                )

            }
        ),

        dcc.Graph(
            id='dividends-payout-ratio-graph',
            figure={
                'data': [go.Bar(x=chart_columns, y=information_df.values[5, 1:], name='Dividends USD'),
                         go.Scatter(x=chart_columns, y=information_df.values[6, 1:], name='Payout Ratio %',
                                    yaxis='y2')
                         ],
                'layout': go.Layout(
                    xaxis={'title': 'Year'},
                    yaxis={'title': 'Dividends USD'},
                    yaxis2={'title': 'Payout Ratio %', 'overlaying': 'y', 'side': 'right'}
                )
            }
        ),
    ])


if __name__ == '__main__':
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    visualize_graph(app)
    app.run_server(debug=True)