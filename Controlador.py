from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

from Interface import Interface

class Controlador:

    def __init__(self):
        self.interface = Interface()
        self.interface.build_indicadores(self.gerar_graficos())
        self.interface.run_interface()


    def gerar_graficos(self):
        self.dados = ''
        with open('dados.json', 'r') as f:
            data = json.load(f)

        with open('id_uf.json', 'r') as f:
            id_uf = json.load(f)

        lista = []

        def graf1():
            df = pd.DataFrame({
                'sex': [x["sexo"] for x in data if x['sexo'] != 'Total' and x["grupo_idade"] == "Total"],
                'qtd': [int(x["populacao"]) for x in data if x['sexo'] != 'Total' and x["grupo_idade"] == "Total"],
                'ano': [x["ano"] for x in data if x['sexo'] != 'Total' and x["grupo_idade"] == "Total"],
                'uf': [x["id_uf"] for x in data if x['sexo'] != 'Total' and x["grupo_idade"] == "Total"],
            })

            fig = px.histogram(df, x="ano", y="qtd", color="sex", barmode="group",histfunc='sum',template="seaborn")
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
                font= {'color': '#FFFFFF'},
                # width = 1200,
                # height = 500
            )

            graf = dcc.Graph(figure=fig)
            return graf

        def graf3():

            df = pd.DataFrame({
                'qtd': [int(x["populacao"]) for x in data if x['sexo'] == 'Total' and x["grupo_idade"] not in (
                    "Total", "60 a 64 anos", "65 anos ou mais", "5 a 13 anos", "14 a 15 anos", "16 a 17 anos") and x[
                            "ano"] == "2019"],
                'idade': [x["grupo_idade"] for x in data if x['sexo'] == 'Total' and x["grupo_idade"] not in (
                    "Total", "60 a 64 anos", "65 anos ou mais", "5 a 13 anos", "14 a 15 anos", "16 a 17 anos") and x[
                              "ano"] == "2019"],
            })
            total = 0
            updated_column = {'idade': []}
            for i in df.values:
                total += i[0]

                if i[1] in ('0 a 4 anos', '5 a 9 anos'):
                    i[1] = '0 a 9 anos'

                elif i[1] in ('10 a 13 anos', '14 a 17 anos', '10 a 13 anos', '18 a 19 anos'):
                    i[1] = '10 a 19 anos'

                elif i[1] in ('20 a 24 anos', '25 a 29 anos'):
                    i[1] = '20 a 29 anos'

                updated_column['idade'].append(i[1])

            new_df = pd.DataFrame(updated_column)
            df.update(new_df)

            fig = px.pie(df, values='qtd', names='idade', title='População Brasileira por Grupo de Idade<br>Total: '+str(total),)
            fig.update_layout(plot_bgcolor='#282d3b',
                paper_bgcolor='#282d3b',
                font= {'color': '#FFFFFF'},
                width = 600,
                height = 500,
            )
            graf = dcc.Graph(figure=fig)
            return graf

        def mapa():
            with open('geoson_br.json', 'r') as file:
                counties = json.load(file)

            df = pd.DataFrame({
                'qtd': [int(x["populacao"]) for x in data
                    if x['sexo'] != 'Total' and x["grupo_idade"] == "Total" and x["ano"] == '2019'],
                'id_uf': [x["id_uf"] for x in data
                    if x['sexo'] != 'Total' and x["grupo_idade"] == "Total" and x["ano"] == '2019'],
            })

            new_df = pd.DataFrame(id_uf)
            df = df.set_index('id_uf').join(new_df.set_index("id_uf"))

            fig = px.choropleth_mapbox(df, geojson=counties, locations='sigla_uf', color='qtd',
                                       color_continuous_scale="Viridis",
                                       range_color=(0, 25000000),
                                       mapbox_style="carto-positron",
                                       zoom=2, center={"lat": -12.319094, "lon": -50.754922},
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

        print("Adicionando indicadores")
        lista.append(graf1())

        ch = html.Div(
            id="banner",
            className="banner",
            children=[
                html.Li(
                    className='nav-item',
                    children=[
                        graf3()
                    ],
                ),
                html.Li(id='espaco-nav',
                    className='nav-item',
                    style={"width":"100px"}
                ),
                html.Li(
                    className='nav-item',
                    children=[
                        mapa()
                    ],
                ),
            ],
        )

        lista.append(ch)
        return lista


if __name__ == '__main__':
    c = Controlador()