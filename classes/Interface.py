# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import html, dcc, dash
from dash.dependencies import Output,Input,State
import plotly.express as px

from classes.AcessarUsuario import AcessarUsuario
from classes.Controlador import Controlador
from classes.Usuario import Usuario


class Interface:

    def __init__(self):
    # assume you have a "long-form" data frame
    # see https://plotly.com/python/px-arguments/ for more options
        self.indicadores = []

        self.controlador = Controlador()

        self.validated = False

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
                    self.usuario = Usuario(uname)
                    self.usuario.set_permissao(i['permissao'])

            if uname == '' or uname == None or passw == '' or passw == None:
                return html.Div(children='', style={'padding-left': '550px', 'padding-top': '10px'})

            elif self.validated:
                return html.Div(dcc.Link('Acesso Permitido!', href='/next_page',
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

        self.build_indicadores()
        self.run_interface()

    def run_interface(self):
        self.app.run_server(debug=True)

    def build_login_page(self):
        return html.Div([
            html.Div(
                dcc.Input(id="user", type="text", placeholder="Usuário",className="inputbox1",
                    style={'margin-left':'35%','width':'450px','height':'45px','padding':'10px','margin-top':'60px',
                    'font-size':'16px','border-width':'3px','border-color':'#a0a3a2'
                }),
            ),
            html.Div(
                dcc.Input(id="passw", type="text", placeholder="Senha",className="inputbox2",
                    style={'margin-left':'35%','width':'450px','height':'45px','padding':'10px','margin-top':'10px',
                    'font-size':'16px','border-width':'3px','border-color':'#a0a3a2',
                }),
            ),
            html.Div(
                html.Button('Entrar', id='verify', n_clicks=0, style={'border-width':'3px','font-size':'14px'}),
                    style={'margin-left':'45%','padding-top':'30px'}),
                html.Div(id='output1')
            ])

    def build_interface(self):
        child = [html.Li(
            id="banner-text",
            className='nav-item',
            children=[
                html.H5("Dashboard Censo"),
                html.H6("Projeto Engenharia de Software"),
            ],
        ), html.Li(id="banner-text",
                   className='nav-item',
                   children=[html.H5("Olá " + self.usuario.nome + '! '),
                             html.H6("Nível de permissao: " + self.usuario.permissao)],
                   )]

        if self.usuario.permissao == '1':
            child.append(html.A('planilha',
                                id='banner-button',
                                className='nav-item button',
                                href='https://docs.google.com/spreadsheets/d/1TXji11jIZMtBK_Li41LNf-oij8PWuWSiGMxuW72njig/edit#gid=0',
                                style={'font-size': '10px', 'border-style': 'solid'}
                                ))

        ch = [html.Div(
            id="banner",
            className="banner",
            children=child,
        )]

        if self.usuario.permissao in ['1', '2']:
            ch.append(html.Div(id="banner",
                className="banner",
                children=[
                    html.Li(id='banner-text', className='nav-item',
                        children=dcc.Dropdown(['10 anos', '20 anos', '30 anos'], 'NYC',
                        id='demo-dropdown')),
                    html.Li(id='banner-text', className='nav-item',
                        children=dcc.Dropdown(['2010', '2011', '2012'], 'NYC', id='demo-dropdown')),
                    html.Li(id='banner-text', className='nav-item',
                        children=dcc.Dropdown(['Todos', 'Feminino', 'Masculino'], 'NYC',
                        id='demo-dropdown')),
                    html.Li(id='banner-text', className='nav-item',
                        children=dcc.Dropdown(['RS', 'SP', 'RJ'], 'NYC', id='demo-dropdown'))
                ])
            )
        # ch = [self.build_banner()]

        for i in self.build_indicadores():
            ch.append(html.Br())
            ch.append(i)
        return html.Div(ch)

    def build_indicadores(self):
        lista = [self.gerar_barra()]

        ch = html.Div(
            id="banner",
            className="banner",
            children=[
                html.Li(
                    className='nav-item',
                    children=[
                        self.gerar_pizza()
                    ],
                ),
                html.Li(id='espaco-nav',
                        className='nav-item',
                        style={"width": "100px"}
                        ),
                html.Li(
                    className='nav-item',
                    children=[
                        self.gerar_mapa()
                    ],
                ),
            ],
        )

        lista.append(ch)

        return lista


    def gerar_mapa(self):

        df = self.controlador.dados_mapa()
        counties = self.controlador.dados_geoson()

        fig = px.choropleth_mapbox(df, geojson=counties, locations='sigla_uf', color='qtd',
                                   color_continuous_scale="Viridis",
                                   range_color=(0, 25000000),
                                   mapbox_style="carto-positron",
                                   zoom=2.8, center={"lat": -14.348643, "lon": -54.089816},
                                   opacity=0.5,
                                   labels={'qtd': 'População'}
                                   )
        fig.update_layout(margin={"r": 20, "t": 20, "l": 20, "b": 20},
            plot_bgcolor='#282d3b',
            paper_bgcolor='#282d3b',
            font={'color': '#FFFFFF'},
            width=600,
            height=500,
        )

        graf = dcc.Graph(figure=fig)
        return graf

    def gerar_pizza(self):
        df = self.controlador.dados_pizza()

        fig = px.pie(df, values='qtd', names='idade',
                     title='População Brasileira por Grupo de Idade')
        fig.update_layout(plot_bgcolor='#282d3b',
                          paper_bgcolor='#282d3b',
                          font={'color': '#FFFFFF'},
                          width=600,
                          height=500,
                          )
        graf = dcc.Graph(figure=fig)
        return graf

    def gerar_barra(self):

        df = self.controlador.dados_barra()

        fig = px.histogram(df, x="ano", y="qtd", color="sex", barmode="group", histfunc='sum', template="seaborn")
        fig.update_layout(
            title='População Brasileira Anual',
            xaxis_tickfont_size=14,
            yaxis=dict(
                title='População',
                titlefont_size=16,
                tickfont_size=14,
                showgrid=False,
            ),
            xaxis=dict(
                title='Ano',
                titlefont_size=16,
                tickfont_size=14,
            ),
            plot_bgcolor='#282d3b',
            paper_bgcolor='#282d3b',
            font={'color': '#FFFFFF'},
            # width = 1200,
            # height = 500
        )

        graf = dcc.Graph(figure=fig)
        return graf
