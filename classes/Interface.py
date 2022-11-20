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
        self.filtro = {'sex': 'Total','idade': 'Total','ano': '2019','uf': 'Total',}
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
                return html.Div(children='> Entre com suas credenciais', style={'padding-left': '400px', 'padding-top': '20px'})

            elif self.validated:
                return html.Div(dcc.Link('> Acesso Permitido. Clique aqui para ver o censo', href='/next_page',
                                        style={'color': 'rgba(10,100,0,100)', 'font-weight': 'bold',
                                                "text-decoration": "none", 'font-size': '16px'}),
                                        style={'padding-left': '400px', 'padding-top': '20px'})
            else:
                return html.Div(children='> Usuário ou senha incorreto',
                                style={'color': 'rgba(90,50,0,100)', 'font-weight': 'bold','padding-left': '400px', 'padding-top': '20px', 'font-size': '16px'})

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

        @self.app.callback(
            Output('filtro_ano', 'children'),
            Input('dropdown_ano', 'value')
        )
        def update_figure_ano(ano):
            self.filtro['ano'] = ano
            # print(self.filtro)
            # return ano

        @self.app.callback(
            Output('filtro_sexo', 'children'),
            Input('dropdown_sexo', 'value')
        )
        def update_figure_sexo(sexo):
            self.filtro['sex'] = sexo
            # print(self.filtro)
            # return sexo

        @self.app.callback(
            Output('filtro_idade', 'children'),
            Input('dropdown_idade', 'value')
        )
        def update_figure_idade(idade):
            self.filtro['idade'] = idade
            # print(self.filtro)
            # return idade

        @self.app.callback(
            Output('filtro_uf', 'children'),
            Input('dropdown_uf', 'value')
        )
        def update_figure_uf(uf):
            self.filtro['uf'] = uf
            # print(self.filtro)
            # return uf

        @self.app.callback(
            Output('indicadores', 'children'),
            Input('Filtrar', 'n_clicks')
        )
        def update_figure_uf(uf):
            # print(self.filtro)
            return self.build_indicadores()

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
                html.Button('Entrar', id='verify', n_clicks=0, style={'border-width':'1px','font-size':'10px'}),
                    style={'margin-left':'35%','padding-top':'30px'}),
                html.Div(id='output1')
            ])

    def build_interface(self):
        child = [
            html.Li(
                id="banner-text",
                className='nav-item',
                children=[
                    html.H4("Dashboard Censo"),
                    html.H6("Projeto Engenharia de Software"),
                ],
            ),
            html.Li(id="banner-text",
                className='nav-item',
                children=[html.H5("Olá " + self.usuario.nome + '! '),
                            html.H6("Nível de permissao: " + self.usuario.permissao)],
            )
        ]

        if self.usuario.permissao == '1':
            child.append(html.A('planilha',
                                id='banner-button',
                                className='nav-item button',
                                href='https://docs.google.com/spreadsheets/d/1TXji11jIZMtBK_Li41LNf-oij8PWuWSiGMxuW72njig/edit#gid=0',
                                target='blank',
                                style={'font-size': '10px', 'border-style': 'solid'}
                                ))

        ch = [html.Div(
            id="banner",
            className="banner",
            children=child,
        )]

        if self.usuario.permissao in ['1', '2']:
            ch.append(self.build_filtro())
        # ch = [self.build_banner()]

        ch.append(html.Div(id='indicadores'))

        return html.Div(ch)

    def build_filtro(self):

        dados_filtro = self.controlador.dados_filtro()

        ch = html.Div(id="banner",
            className="banner",
            children=[
                html.Li(className='nav-item',style={"width": "200px"},
                    children=[html.Div('Ano'),
                        dcc.Dropdown(dados_filtro['ano'],dados_filtro['ano'][0],id='dropdown_ano',clearable=False),
                        html.Div(id='filtro_ano')]),

                html.Li(className='nav-item',style={"width": "200px"},
                    children=[html.Div('Sexo'),
                        dcc.Dropdown(dados_filtro['sex'],dados_filtro['sex'][0], id='dropdown_sexo',clearable=False),
                        html.Div(id='filtro_sexo')]),

                html.Li(className='nav-item',style={"width": "200px"},
                    children=[html.Div('Faixa Etária'),
                        dcc.Dropdown(dados_filtro['idade'],dados_filtro['idade'][0],id='dropdown_idade',clearable=False),
                        html.Div(id='filtro_idade')]),

                html.Li(className='nav-item',style={"width": "200px"},
                    children=[html.Div('Estado'),
                        dcc.Dropdown(options=dados_filtro['uf'],value=dados_filtro['uf'][0]['value'], id='dropdown_uf',clearable=False),
                        html.Div(id='filtro_uf')]),

                html.Button('Filtrar', id='Filtrar', n_clicks=0, style={'margin-top':'12px','font-size': '10px', 'border-style': 'solid'}),
        ])

        return ch

    def gerar_indicadores(self):
        self.gerar_barra()
        self.gerar_pizza()
        self.gerar_mapa()

    def build_indicadores(self):
        self.gerar_indicadores()

        lista = [self.graf_barra]

        ch = html.Div(
            id="banner",
            className="banner",
            style={'padding-top':'10px','padding-left':'0px','padding-right':'0px'},
            children=[
                html.Li(
                    className='nav-item',
                    children=[
                        self.graf_pizza
                    ],
                ),
                html.Li(
                    className='nav-item',
                    children=[
                        self.graf_mapa
                    ],
                ),
            ],
        )

        lista.append(ch)

        div = html.Div(children=lista, style={'padding-top':'10px','padding-left':'20px','padding-right':'20px'})

        return div
    
    def gerar_mapa(self):
        sex_ = self.filtro['sex']
        ano_ = self.filtro['ano']
        idade_ = self.filtro['idade']
        uf_ = self.filtro['uf']

        df = self.controlador.dados_mapa(ano=ano_,sexo=sex_,idade=idade_,uf=uf_)
        counties = self.controlador.dados_geoson()

        fig = px.choropleth_mapbox(df, geojson=counties, locations='sigla_uf', color='qtd',
                                   color_continuous_scale="jet",
                                   range_color=(df['qtd'].min()-100000, df['qtd'].max()),
                                   mapbox_style="carto-positron",
                                   zoom=2.8, center={"lat": -14.348643, "lon": -54.089816},
                                   opacity=0.5,
                                   labels={'qtd': 'População'}
                                   )
        fig.update_layout(margin={"r": 20, "t": 20, "l": 20, "b": 20},
            plot_bgcolor='#282d3b',
            paper_bgcolor='#282d3b',
            font={'color': '#FFFFFF'},
            width=550,
            height=500,
        )

        graf = dcc.Graph(figure=fig)
        self.graf_mapa = graf

    def gerar_pizza(self):

        sex_ = self.filtro['sex']
        ano_ = self.filtro['ano']
        idade_ = self.filtro['idade']
        uf_ = self.filtro['uf']

        df = self.controlador.dados_pizza(ano=ano_,sexo=sex_,idade=idade_,uf=uf_)

        fig = px.pie(df, values='qtd', names='idade',
                     title='População Brasileira por Grupo de Idade')
        fig.update_layout(plot_bgcolor='#282d3b',
                          paper_bgcolor='#282d3b',
                          font={'color': '#FFFFFF'},
                          width=500,
                          height=500,
                          )
        graf = dcc.Graph(figure=fig)
        self.graf_pizza = graf

    def gerar_barra(self):

        sex_ = self.filtro['sex']
        ano_ = self.filtro['ano']
        idade_ = self.filtro['idade']
        uf_ = self.filtro['uf']

        df = self.controlador.dados_barra(ano=ano_,sexo=sex_,idade=idade_,uf=uf_)

        fig = px.histogram(df, x="Ano", y="Qtd",
                            color="Sexo",
                            barmode="group",
                            histfunc='sum',
                            opacity=0.9,
                            color_discrete_sequence=["blue","green"],
                            text_auto=True)
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
                showgrid=False,
            ),
            plot_bgcolor='#282d3b',
            paper_bgcolor='#282d3b',
            font={'color': '#FFFFFF'},
            bargroupgap=0.1
            # width = 1200,
            # height = 500
        )

        graf = dcc.Graph(figure=fig)
        self.graf_barra = graf
