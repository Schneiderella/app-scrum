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

        with open('classes/data/geoson_br.json', 'r') as file:
            self.counties = json.load(file)

    def tratar_dados(self):
        data_2 = self.data

        del_index = []
        i = 0

        # Altera valor de alguns campos para ficar com os períodos certinhos de 10 anos e não quebrados
        while i < len(data_2):
            # print(self.data[i]["grupo_idade"])

            if data_2[i]["grupo_idade"] in ('0 a 4 anos', '5 a 9 anos'):
                data_2[i]["grupo_idade"] = '0 a 9 anos'

            elif data_2[i]["grupo_idade"] in ('10 a 13 anos', '14 a 17 anos', '10 a 13 anos', '18 a 19 anos'):
                data_2[i]["grupo_idade"] = '10 a 19 anos'

            elif data_2[i]["grupo_idade"] in ('20 a 24 anos', '25 a 29 anos'):
                data_2[i]["grupo_idade"] = '20 a 29 anos'


            if data_2[i]["grupo_idade"] in ("60 a 64 anos", "65 anos ou mais", "5 a 13 anos", "14 a 15 anos", "16 a 17 anos"):
                # Adiciona a lista de indices a serem deletados
                del_index.append(i)

            i += 1

        # deleta os valores dos indices a serem deletados
        cont = 0
        for i in del_index:
            # print(i,cont)
            del data_2[i-cont]
            cont += 1

        self.data = data_2

    # retorna os dados tratados a serem utilizados no graf de barras
    def dados_barra(self, sexo=['Homens','Mulheres'], idade='Total', ano='2019', uf='Total'):

        condicao = lambda x: x['sexo'] in ['Homens','Mulheres'] and x["grupo_idade"] == idade
        if uf != 'Total':
            condicao = lambda x: x['sexo'] in ['Homens','Mulheres'] and x["grupo_idade"] == idade and x["id_uf"] == uf

        df = pd.DataFrame({
            'Sexo': [x["sexo"] for x in self.data if condicao(x)],
            'Qtd': [int(x["populacao"]) for x in self.data if condicao(x)],
            'Ano': [x["ano"] for x in self.data if condicao(x)],
            'Uf': [x["id_uf"] for x in self.data if condicao(x)],
        })

        return df

    # retorna os dados tratados a serem utilizados no graf de pizza
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

    def dados_geoson(self):

        return self.counties

    def dados_filtro(self):
        dados = {
            'sex': sorted(list(set([x["sexo"] for x in self.data]))),
            'ano': sorted(list(set([x["ano"] for x in self.data])), reverse=True),
            'idade': sorted(list(set([x["grupo_idade"] for x in self.data]))),
            'uf': [
            ]
        }
        dados['sex'].remove('Total')
        dados['idade'].remove('Total')

        for i in self.data:
            for j in self.id_uf:
                if i['id_uf'] == j['id_uf']:
                    dados['uf'].append({'value': i['id_uf'], 'label': j['sigla_uf']})

        dados['uf'] = self.unique(dados['uf'])

        dados['uf'] = sorted(dados['uf'],key=lambda x: x['label'])

        dados['uf'].insert(0, {'value': 'Total', 'label': 'Total'})
        dados['sex'].insert(0, 'Total')
        dados['idade'].insert(0, 'Total')

        return dados

    @staticmethod
    def unique(list1):
        # initialize a null list
        unique_list = []

        # traverse for all elements
        for x in list1:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)
        # print list
        return unique_list
