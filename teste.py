from classes.Controlador import Controlador


if __name__ == '__main__':
    c = Controlador()
    print(c.dados_mapa()['qtd'].sum())