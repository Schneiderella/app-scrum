import pandas as pd
import json


class Controlador:

    def __init__(self):
        with open('classes/data/dados.json', 'r') as f:
            self.data = json.load(f)
            # print(self.data)

        self.tratar_dados()

        with open('classes/data/id_uf.json', 'r') as f:
            self.id_uf = json.load(f)

    def tratar_dados(self):
        data_2 = self.data

        del_index = []
        i = 0
        while i < len(data_2):
            # print(self.data[i]["grupo_idade"])

            if data_2[i]["grupo_idade"] in ('0 a 4 anos', '5 a 9 anos'):
                data_2[i]["grupo_idade"] = '0 a 9 anos'

            elif data_2[i]["grupo_idade"] in ('10 a 13 anos', '14 a 17 anos', '10 a 13 anos', '18 a 19 anos'):
                data_2[i]["grupo_idade"] = '10 a 19 anos'

            elif data_2[i]["grupo_idade"] in ('20 a 24 anos', '25 a 29 anos'):
                data_2[i]["grupo_idade"] = '20 a 29 anos'

            if data_2[i]["grupo_idade"] in ("60 a 64 anos", "65 anos ou mais", "5 a 13 anos", "14 a 15 anos", "16 a 17 anos"):
                del_index.append(i)

            i += 1

        cont = 0
        for i in del_index:
            # print(i,cont)
            del data_2[i-cont]
            cont += 1

        self.data = data_2

    def dados_barra(self, sexo=['Homens','Mulheres'], idade='Total', ano='2019', uf='Total'):

        condicao = lambda x: x['sexo'] in ['Homens','Mulheres'] and x["grupo_idade"] == idade
        if uf != 'Total':
            condicao = lambda x: x['sexo'] in ['Homens','Mulheres'] and x["grupo_idade"] == idade and x["id_uf"] == uf

        df = pd.DataFrame({
            'sex': [x["sexo"] for x in self.data if condicao(x)],
            'qtd': [int(x["populacao"]) for x in self.data if condicao(x)],
            'ano': [x["ano"] for x in self.data if condicao(x)],
            'uf': [x["id_uf"] for x in self.data if condicao(x)],
        })

        return df

    def dados_pizza(self, sexo='Total', idade='Total', ano='2019', uf='Total'):

        condicao = lambda x: x['sexo'] == sexo and x["ano"] == ano and x["grupo_idade"] != 'Total'
        if uf != 'Total':
            condicao = lambda x: x['sexo'] == sexo and x["ano"] == ano and x["grupo_idade"] != 'Total' and x["id_uf"] == uf

        df = pd.DataFrame({
            'qtd': [int(x["populacao"]) for x in self.data if condicao(x)],
            'idade': [x["grupo_idade"] for x in self.data if condicao(x)],
        })

        return df

    def dados_mapa(self, sexo='Total', idade='Total', ano='2019', uf='Total'):

        condicao = lambda x: x['sexo'] == sexo and x["ano"] == ano and x["grupo_idade"] == idade
        if uf != 'Total':
            condicao = lambda x: x['sexo'] == sexo and x["ano"] == ano and x["grupo_idade"] == idade and x["id_uf"] == uf

        df = pd.DataFrame({
            'qtd': [int(x["populacao"]) for x in self.data if condicao(x)],
            'id_uf': [x["id_uf"] for x in self.data if condicao(x)],
        })

        new_df = pd.DataFrame(self.id_uf)
        df = df.set_index('id_uf').join(new_df.set_index("id_uf"))

        return df

    @staticmethod
    def dados_geoson():
        with open('classes/data/geoson_br.json', 'r') as file:
            counties = json.load(file)

        return counties
