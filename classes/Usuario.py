class Usuario:

    def __init__(self, nome, permissao=1):
        self.nome = nome
        self.permissao = permissao

    def set_permissao(self, permissao):
        self.permissao = permissao
