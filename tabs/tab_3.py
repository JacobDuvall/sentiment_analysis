import dash
import dash_core_components as dcc
import dash_html_components as html
import pyodbc
import database as db

candidates = db.select_database("SELECT name FROM Candidate WHERE date_dropped != ")

tab_3_layout = html.Div([
    html.H1('Page 3'),
    dcc.Checklist(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value=['MTL', 'SF']
    )
])
