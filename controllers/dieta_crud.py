import sys
sys.path.append("../model")
from model.model import Dieta
from peewee import fn


def ler_refeicoes_dieta(dieta):
    try:
        return dieta.refeicoes
    except:
        return None

def quantidade_dietas():
    return Dieta.select().count()

def busca_dietas(nome):
    try:
        
        dieta = Dieta.select().where(fn.lower(Dieta.nome).contains(nome))
        return dieta
    except:
        return None

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

def ler_dietas(paginacao=False, items_por_pagina=10, pagina=1):
    """
    Lê todas as dietas no banco de dados.

    Returns:
        list: Uma lista de objetos Dieta representando todas as dietas no banco de dados,
            ou None se ocorreu um erro ao acessar o banco de dados.
    """

    try:
        dietas = Dieta.select().order_by(Dieta.nome)
        if paginacao:
            dietas = dietas.paginate(pagina, items_por_pagina)

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
        dieta = Dieta.select().where(fn.lower(Dieta.nome).contains(nome)).get()
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
        if "calorias_totais" in campos:
            dieta_buscada.calorias_totais = dieta["calorias_totais"]
        if "proteinas_totais" in campos:
            dieta_buscada.proteinas_totais = dieta["proteinas_totais"]
        if "gorduras_totais" in campos:
            dieta_buscada.gorduras_totais = dieta["gorduras_totais"]
        if "carboidratos_totais" in campos:
            dieta_buscada.carboidratos_totais = dieta["carboidratos_totais"]   
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
    bool: Retorna True se a refeicao foi adicionada com sucesso, caso contrário, retorna False
    """

    try:
        dieta.refeicoes.add(refeicao)
        return True
    except Exception as e:
        print("add_refeicao: ", e)
        return False

def calcula_informacoes_nutricionais(dieta):

    try:
        refeicoes = dieta.refeicoes
        refeicoes = [refeicao for refeicao in refeicoes]
        
        dieta_atualizada = {
            "calorias_totais": 0,
            "gorduras_totais": 0,
            "proteinas_totais": 0,
            "carboidratos_totais": 0
        }

        for refeicao in refeicoes:
            dieta_atualizada["calorias_totais"] += refeicao.calorias_totais if refeicao.calorias_totais is not None else 0
            dieta_atualizada["gorduras_totais"] += refeicao.gorduras_totais if refeicao.gorduras_totais is not None else 0
            dieta_atualizada["proteinas_totais"] += refeicao.proteinas_totais if refeicao.proteinas_totais is not None else 0
            dieta_atualizada["carboidratos_totais"] += refeicao.carboidratos_totais if refeicao.carboidratos_totais is not None else 0
        
        atualizar_dieta(dieta.nome, dieta_atualizada)
        return True
    except Exception as e:
        print(f"Erro: {e}")
        return False
    
    
def remove_refeicao(dieta, refeicao):
    """
    Remove uma refeição de uma dieta, falando em banco de dados, deleta uma linha na tabela de relação ManyToMany

    Args:
    dieta (Model): Objeto da dieta que será deletado a refeição
    refeicao (Model): Objeto do refeição que será deletado da dieta

    Returns:
    bool: Retorna True se a refeição foi deletado com sucesso, caso contrário, retorna False
    """
    try:
        dieta.refeicoes.remove(refeicao)
        dieta.save()
        return True
    except Exception as e:
        print(f"{e}")
        return False