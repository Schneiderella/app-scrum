import pandas as pd
import json


class Controlador:

    def __init__(self):
        with open('dados.json', 'r') as f:
            self.data = json.load(f)

        with open('id_uf.json', 'r') as f:
            self.id_uf = json.load(f)

    def dados_barra(self):

        df = pd.DataFrame({
            'sex': [x["sexo"] for x in self.data if x['sexo'] != 'Total' and x["grupo_idade"] == "Total"],
            'qtd': [int(x["populacao"]) for x in self.data if x['sexo'] != 'Total' and x["grupo_idade"] == "Total"],
            'ano': [x["ano"] for x in self.data if x['sexo'] != 'Total' and x["grupo_idade"] == "Total"],
            'uf': [x["id_uf"] for x in self.data if x['sexo'] != 'Total' and x["grupo_idade"] == "Total"],
        })

        return df

    def dados_pizza(self):

        df = pd.DataFrame({
            'qtd': [int(x["populacao"]) for x in self.data if x['sexo'] == 'Total' and x["grupo_idade"] not in (
                "Total", "60 a 64 anos", "65 anos ou mais", "5 a 13 anos", "14 a 15 anos", "16 a 17 anos") and x[
                        "ano"] == "2019"],
            'idade': [x["grupo_idade"] for x in self.data if x['sexo'] == 'Total' and x["grupo_idade"] not in (
                "Total", "60 a 64 anos", "65 anos ou mais", "5 a 13 anos", "14 a 15 anos", "16 a 17 anos") and x[
                          "ano"] == "2019"],
        })
        updated_column = {'idade': []}
        for i in df.values:

            if i[1] in ('0 a 4 anos', '5 a 9 anos'):
                i[1] = '0 a 9 anos'

            elif i[1] in ('10 a 13 anos', '14 a 17 anos', '10 a 13 anos', '18 a 19 anos'):
                i[1] = '10 a 19 anos'

            elif i[1] in ('20 a 24 anos', '25 a 29 anos'):
                i[1] = '20 a 29 anos'

            updated_column['idade'].append(i[1])

        new_df = pd.DataFrame(updated_column)
        df.update(new_df)

        return df

    def dados_mapa(self):

        df = pd.DataFrame({
            'qtd': [int(x["populacao"]) for x in self.data
                    if x['sexo'] != 'Total' and x["grupo_idade"] == "Total" and x["ano"] == '2019'],
            'id_uf': [x["id_uf"] for x in self.data
                      if x['sexo'] != 'Total' and x["grupo_idade"] == "Total" and x["ano"] == '2019'],
        })

        new_df = pd.DataFrame(self.id_uf)
        df = df.set_index('id_uf').join(new_df.set_index("id_uf"))

        return df

    @staticmethod
    def dados_geoson():
        with open('geoson_br.json', 'r') as file:
            counties = json.load(file)

        return counties




