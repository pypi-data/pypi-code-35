import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

import pandas as pd


navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            nav=True,
            caret=False,
            in_navbar=True,
            label='Aperture',
            direction='right',
            children=[
                dbc.DropdownMenuItem('Home'),
                dbc.DropdownMenuItem('My Profile'),
                dbc.DropdownMenuItem('Sign out')
            ]
        )
    ],
    sticky='top',
    brand='Contenders'
)


class GameMode(dbc.Card):
    buttons = [
        dbc.Button('Create Game', color='primary', className='mr-1 float-left'),
        dbc.Button('Join Game', color='success', className='mr-1 float-right')
    ]

    @classmethod
    def card(self, name: str, description: str):
        return dbc.Card([
            dbc.CardHeader(name),
            dbc.CardBody(description),
            dbc.CardFooter(self.buttons)
        ])


cards = dbc.CardDeck(
    [
        GameMode.card('Code Golf', 'Submit a working solution with the lowest byte count.'),
        GameMode.card('Fastest Solution', 'Submit a working solution as fast as possible.')
    ],
    style={'text-align': 'center'}
)

df = pd.read_csv('contenders/scores.csv')

scoreboard = dbc.Table.from_dataframe(
    df, hover=True, style={'margin-top': '1rem'}
)

body = dbc.Container([cards, scoreboard], className="mt-4")

app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP]
)
app.layout = html.Div([navbar, body])
