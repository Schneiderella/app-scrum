# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, dash
from dash.dependencies import Output,Input,State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash_auth import BasicAuth
import dash_enterprise_auth as auth

from AcessarUsuario import AcessarUsuario
from Usuario import Usuario


class Interface:

    def __init__(self):
    # assume you have a "long-form" data frame
    # see https://plotly.com/python/px-arguments/ for more options
        self.login_page = ''
        self.interface = ''
        self.indicadores = []

        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css','https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css']
        self.app = dash.Dash(__name__, suppress_callback_exceptions=True,external_stylesheets=external_stylesheets)

        self.app.layout = html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content')
        ])

        @self.app.callback(
            Output('output1', 'children'),
            [Input('verify', 'n_clicks')],
            [State('user', 'value'), State('passw', 'value')]
        )
        def update_output(n_clicks, uname, passw):
            li = AcessarUsuario.extract_table()
            self.validated = False
            for i in li:
                if i['nome'] == uname and i['pword'] == passw:
                    self.validated = True
                    self.Usuario = Usuario(uname)
                    self.Usuario.set_permissao(i['permissao'])

            if uname == '' or uname == None or passw == '' or passw == None:
                return html.Div(children='', style={'padding-left': '550px', 'padding-top': '10px'})

            elif self.validated:
                return html.Div(dcc.Link('Access Granted!', href='/next_page',
                                        style={'color': '#183d22', 'font-family': 'serif', 'font-weight': 'bold',
                                                "text-decoration": "none", 'font-size': '20px'}),
                                        style={'padding-left': '605px', 'padding-top': '40px'})
            else:
                return html.Div(children='Usuário ou senha incorreto',
                                style={'padding-left': '550px', 'padding-top': '40px', 'font-size': '16px'})

        @self.app.callback(
                Output('page-content', 'children'),
                [Input('url', 'pathname')]
        )
        def display_page(pathname):
            if pathname == '/next_page' and self.validated:
                # return self.build_interface()
                return self.build_interface()
            if pathname == '/next_page' and not self.validated:
                return html.Div(dcc.Link('Login Necessário!', href='/',
                                        style={'color': '#183d22', 'font-family': 'serif', 'font-weight': 'bold',
                                                "text-decoration": "none", 'font-size': '20px'}),
                                        style={'padding-left': '605px', 'padding-top': '40px'})
            else:
                return self.build_login_page()

    def run_interface(self):
        self.app.run_server()

    def build_login_page(self):
        return html.Div([
            html.Div(
                dcc.Input(id="user", type="text", placeholder="Enter Username",className="inputbox1",
                    style={'margin-left':'35%','width':'450px','height':'45px','padding':'10px','margin-top':'60px',
                    'font-size':'16px','border-width':'3px','border-color':'#a0a3a2'
                }),
            ),
            html.Div(
                dcc.Input(id="passw", type="text", placeholder="Enter Password",className="inputbox2",
                    style={'margin-left':'35%','width':'450px','height':'45px','padding':'10px','margin-top':'10px',
                    'font-size':'16px','border-width':'3px','border-color':'#a0a3a2',
                }),
            ),
            html.Div(
                html.Button('Verify', id='verify', n_clicks=0, style={'border-width':'3px','font-size':'14px'}),
                    style={'margin-left':'45%','padding-top':'30px'}),
                html.Div(id='output1')
            ])

    def build_interface(self):
        ch = [html.Div(
            id="banner",
            className="banner",
            children=[
                html.Li(
                    id="banner-text",
                    className='nav-item',
                    children=[
                        html.H5("Dashboard Censo"),
                        html.H6("Projeto Engenharia de Software"),
                    ],
                ),html.Li(id="banner-text",
                    className='nav-item',
                    children=[html.H5("Olá "+self.Usuario.nome+'! '),
                        html.H6("Nível de permissao: "+self.Usuario.permissao)],
                ),
                html.A('planilha',
                    id='banner-button',
                    className='nav-item button',
                    href='https://docs.google.com/spreadsheets/d/1TXji11jIZMtBK_Li41LNf-oij8PWuWSiGMxuW72njig/edit#gid=0',
                    style={'font-size': '10px','border-style': 'solid'}
                ),
            ],
        )]
        # ch = [self.build_banner()]
        for i in self.indicadores:
            ch.append(html.Br())
            ch.append(i)
        return html.Div(ch)

    def build_indicadores(self,indicadores):
        self.indicadores = indicadores





