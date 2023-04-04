import sys
sys.path.append("../model")
from model.model import Dieta

def criar_dieta(dieta):
    """
    Cria uma nova dieta no banco de dados.

    Args:
        dieta (dict): Um dicionário contendo informações sobre a dieta.
            Deve conter as chaves 'nome' e 'descricao'.

    Returns:
        bool: True se a dieta foi criada com sucesso, False caso contrário.

    """
    try:
        Dieta.create(
            nome=dieta["nome"],
            descricao=dieta["descricao"]
        )
        return True
    except:
        return False

def ler_dietas():
    """
    Lê todas as dietas no banco de dados.

    Returns:
        list: Uma lista de objetos Dieta representando todas as dietas no banco de dados,
            ou None se ocorreu um erro ao acessar o banco de dados.
    """

    try:
        dietas = Dieta.select()
        return dietas
    except:
        return None

def ler_dieta(nome):
    """
    Lê uma dieta específica no banco de dados.

    Args:
        nome (str): O nome da dieta que deve ser lida.

    Returns:
        Dieta: Um objeto Dieta representando a dieta com o nome especificado,
            ou None se a dieta não pôde ser encontrada ou ocorreu um erro ao acessar o banco de dados.
    """

    try:
        dieta = Dieta.select().where(Dieta.nome == nome).get()
        return dieta
    except:
        return None

def atualizar_dieta(nome, dieta):
    """
    Atualiza as informações de uma dieta no banco de dados.

    Args:
        nome (str): O nome da dieta que deve ser atualizada.
        dieta (dict): Um dicionário contendo informações atualizadas sobre a dieta.
            Pode conter algumas ou todas as chaves que o dicionário de criação de dietas tem.

    Returns:
        bool: True se a dieta foi atualizada com sucesso, False caso contrário.
    """
    try:
        dieta_buscada = Dieta.select().where(Dieta.nome == nome).get()
        campos = dieta.keys()
        if "nome" in campos:
            dieta_buscada.nome = dieta["nome"]
        if "descricao" in campos:
            dieta_buscada.descricao = dieta["descricao"]
        dieta_buscada.save()
        return True
    except:
        return False

def deletar_dieta(nome):
    """
    Deleta um objeto da classe Dieta do banco de dados com o nome especificado.

    Args:
    nome (str): O nome da dieta a ser deletada.

    Returns:
    bool: Retorna True se a dieta foi deletada com sucesso do banco de dados, caso contrário, retorna False.
    """
     
    try:
        dieta = Dieta.select().where(Dieta.nome == nome).get()
        dieta.delete_instance()
        return True
    except:
        return False


def add_refeicao(refeicao, dieta):
    """
    Adiciona uma refeicao em uma dieta, falando em banco de dados, cria uma nova linha na tabela de relação ManyToMany

    Args:
    refeicao (Model): Objeto da refeicao que será adicionado o refeicao
    dieta (Model): Objeto da dieta que será adicionado a refeição

    Returns:
    bool: Retorna True se a dieta foi criado com sucesso, caso contrário, retorna False
    """

    try:
        dieta.refeicoes.add(refeicao)
        return True
    except:
        return False