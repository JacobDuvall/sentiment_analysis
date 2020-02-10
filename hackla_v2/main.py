import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from tabs import tab_1, tab_2, tab_3, tab_4, tab_5
import sqlite3
import plotly.graph_objs as go
import pandas as pd
import plotly
import database as db
import numpy as np

app = dash.Dash()

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.H1('Boys Rule ROFLCOPTER'),
dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Tab One', value='tab-1-example'),
        dcc.Tab(label='Tab Two', value='tab-2-example'),
        dcc.Tab(label='Tab Three', value='tab-3-example'),
        dcc.Tab(label='Tab Four', value='tab-4-example'),
        dcc.Tab(label='Tab Five', value='tab-5-example')
    ]),
    html.Div(id='tabs-content-example')
])

# DO NOT TOUCH
@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return tab_1.tab_1_layout
    elif tab == 'tab-2-example':
        return tab_2.tab_2_layout
    elif tab == 'tab-3-example':
        return tab_3.tab_3_layout
    elif tab == 'tab-4-example':
        return tab_4.tab_4_layout
    elif tab == 'tab-5-example':
        return tab_5.tab_5_layout

# Tab 1 callback -- ALEX
@app.callback(Output('live-graph', 'figure'),
              [Input('term', 'value'), Input('graph-update', 'n_intervals')])
def update_graph_scatter(term, ignore):
    try:
        conn = sqlite3.connect('C:\\Users\\Olive\\PycharmProjects\\hacklahoma\\twitter.db')
        c = conn.cursor()
        df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 1000",
                         conn,
                         params=('%' + term + '%',))
        df.sort_values('unix', inplace=True)
        df['sentiment_smoothed'] = df['sentiment'].rolling(int(len(df)/5)).mean()
        df.dropna(inplace=True)

        X = df.unix.values[-100:]
        Y = df.sentiment_smoothed.values[-100:]

        data = plotly.graph_objs.Scatter(
                x=X,
                y=Y,
                name='Scatter',
                mode='lines+markers'
                )

        return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                                    yaxis=dict(range=[min(Y), max(Y)]),)}

    except Exception as e:
        with open('errors.txt', 'a') as f:
            f.write(str(e))
            f.write('\n')

# Tab 2 callback -- ERIC
@app.callback(Output('page-2-content', 'children'),
              [Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)

# Tab 3 callback -- JACOB
@app.callback(Output('box-graph', 'figure'),
              [Input('candidate-dropdown', 'value'), Input('metric-dropdown', 'value')])
def page_3_booyah(candidates, metric):
    guys = list()
    gals = list()
    rule = list()
    if candidates:
        for i in candidates:
            query = "SELECT " + str(metric) + " FROM Twitter_Metrics " + "WHERE [name] = '" + str(i) + "'"
            the_goods = db.select_database(query)

            guys.append(i)
            gals.append(the_goods[metric].values[0])

        data = plotly.graph_objs.Bar(
            x=guys,
            y=gals,
            name='Bar'
        )

        return {'data': [data], 'layout': go.Layout(xaxis=dict(range=(0-1, len(guys))),
                                                    yaxis=dict(range=[0, max(gals)]), )}

    all_info_baby = {
        'x': [],
        'y': [],
        'type': 'bar'
    }
    layout = {
        'xaxis': {'title': 'Candidate'},
        'yaxis': {'title': 'Y axis'},
        'barmode': 'relative',
        'title': metric
    };
    rule.append(all_info_baby)

    return {'data': rule, 'layout': layout}

# Tab 4 callback
@app.callback(Output('page-4-content', 'children'),
              [Input('page-4-radios', 'value')])
def page_4_radios(value):
    return 'You have selected "{}"'.format(value)

# Tab 5 callback
@app.callback(Output('line-graph', 'figure'),
              [Input('candidate-dropdown', 'value')])
def page_5_radios(candidates):
    try:
        lines = list()
        if candidates:
            print(candidates)
            for i in candidates:
                query = "SELECT sentiment_date, ((positive_tweet_count * 1.) / " \
                        + "(positive_tweet_count + negative_tweet_count + neutral_tweet_count)) * 100. as score" \
                        + " FROM Candidate_Sentiment" \
                        + " WHERE name = '" \
                        + str(i) \
                        + "';"

                dates = list()
                score = list()

                the_goods = db.select_database(query)

                for index, row in the_goods.iterrows():
                    dates.append(row['sentiment_date'])
                    score.append(row['score'])
                lines.append(plotly.graph_objs.Scatter(
                    x=np.asarray(dates),
                    y=np.asarray(score),
                    name=i,
                    mode='lines+markers'
                    ))
                print(lines)
            data = lines
            lines = list()
            layout = dict(title='Candidate Sentiment By Date',
                          xaxis=dict(title='Date'),
                          yaxis=dict(title='Sentiment Score -- (0-100%)'),
                          )

            return {'data': data, 'layout': layout}
        else:
            data = {
                'x': [],
                'y': [],
                'type': 'line'
            }
            layout = dict(title='Candidate Sentiment By Date',
                          xaxis=dict(title='Date'),
                          yaxis=dict(title='Sentiment Score -- (0-100%)'),
                          )
            return {'data': [data], 'layout': layout}

    except Exception as e:
        with open('errors.txt', 'a') as f:
            f.write(str(e))
            f.write('\n')




app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)