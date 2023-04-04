import sys
sys.path.append("/home/mrbushido/Documentos/programacao/NutriApp")
from model.model import Alimento
from peewee import fn

def busca_alimentos(nome):
    try:
        alimento = Alimento.select().where(fn.lower(Alimento.nome).contains(nome.lower()))
        return alimento
    except:
        return None

def quantidade_alimentos():
    return Alimento.select().count()

def criar_alimento(alimento):
    """
    Cria um novo alimento no banco de dados.

    Args:
        alimento (dict): Um dicionário contendo informações sobre o alimento.
            Deve conter as chaves 'nome', 'calorias_por_grama', 'calorias_por_colher',
            'calorias_por_ml', 'proteinas_por_grama', 'carboidratos_por_grama',
            'gorduras_por_grama' e 'descricao'.

    Returns:
        bool: True se o alimento foi criado com sucesso, False caso contrário.

    """
    try:
        Alimento.create(
            nome=alimento["nome"],
            calorias_por_grama=alimento["calorias_por_grama"],
            calorias_por_colher=alimento["calorias_por_colher"],
            calorias_por_ml=alimento["calorias_por_ml"],
            proteinas_por_grama=alimento["proteinas_por_grama"],
            carboidratos_por_grama=alimento["carboidratos_por_grama"],
            gorduras_por_grama=alimento["gorduras_por_grama"],
            proteinas_por_ml=alimento["proteinas_por_ml"],
            carboidratos_por_ml=alimento["carboidratos_por_ml"],
            gorduras_por_ml=alimento["gorduras_por_ml"],
            proteinas_por_colher=alimento["proteinas_por_colher"],
            carboidratos_por_colher=alimento["carboidratos_por_colher"],
            gorduras_por_colher=alimento["gorduras_por_colher"],
            descricao=alimento["descricao"]
        )
        return True
    except:
        return False

def ler_alimentos(paginacao=False, items_por_pagina=10, pagina=1):
    """
    Lê todos os alimentos no banco de dados.

    Returns:
        list: Uma lista de objetos Alimento representando todos os alimentos no banco de dados,
            ou None se ocorreu um erro ao acessar o banco de dados.
    """

    try:
        alimentos = Alimento.select().order_by(Alimento.nome)
        if paginacao:
            alimentos = alimentos.paginate(pagina, items_por_pagina)
        return alimentos
    except:
        return None

def ler_alimento(nome):
    """
    Lê um alimento específico no banco de dados.

    Args:
        nome (str): O nome do alimento que deve ser lido.

    Returns:
        Alimento: Um objeto Alimento representando o alimento com o nome especificado,
            ou None se o alimento não pôde ser encontrado ou ocorreu um erro ao acessar o banco de dados.
    """

    try:
        alimento = Alimento.select().where(Alimento.nome == nome).get()
        return alimento
    except:
        return None

def atualizar_alimento(nome, alimento):
    """
    Atualiza as informações de um alimento no banco de dados.

    Args:
        nome (str): O nome do alimento que deve ser atualizado.
        alimento (dict): Um dicionário contendo informações atualizadas sobre o alimento.
            Pode conter algumas ou todas as chaves que o dicionário de criação de alimentos tem.

    Returns:
        bool: True se o alimento foi atualizado com sucesso, False caso contrário.
    """
    try:
        campos = alimento.keys()
        alimento_buscado = ler_alimento(nome)
        if "nome" in campos:
            alimento_buscado.nome = alimento["nome"]
        if "calorias_por_grama" in campos:
            alimento_buscado.calorias_por_grama = alimento["calorias_por_grama"]
        if "calorias_por_colher" in campos:
            alimento_buscado.calorias_por_colher = alimento["calorias_por_colher"]
        if "calorias_por_ml" in campos:
            alimento_buscado.calorias_por_ml = alimento["calorias_por_ml"]
        if "proteinas_por_grama" in campos:
            alimento_buscado.proteinas_por_grama = alimento["proteinas_por_grama"]
        if "carboidratos_por_grama" in campos:
            alimento_buscado.carboidratos_por_grama = alimento["carboidratos_por_grama"]
        if "gorduras_por_grama" in campos:
            alimento_buscado.gorduras_por_grama = alimento["gorduras_por_grama"]
        if "proteinas_por_colher" in campos:
            alimento_buscado.proteinas_por_colher = alimento["proteinas_por_colher"]
        if "carboidratos_por_colher" in campos:
            alimento_buscado.carboidratos_por_colher = alimento["carboidratos_por_colher"]
        if "gorduras_por_colher" in campos:
            alimento_buscado.gorduras_por_colher = alimento["gorduras_por_colher"]
        if "proteinas_por_ml" in campos:
            alimento_buscado.proteinas_por_ml = alimento["proteinas_por_ml"]
        if "carboidratos_por_ml" in campos:
            alimento_buscado.carboidratos_por_ml = alimento["carboidratos_por_ml"]
        if "gorduras_por_ml" in campos:
            alimento_buscado.gorduras_por_ml = alimento["gorduras_por_ml"]    
        if "descricao" in campos:
            alimento_buscado.descricao = alimento["descricao"]
        alimento_buscado.save()
        return True
    except Exception as e:
        print(e)
        return False

def deletar_alimento(nome):
    """
    Deleta um objeto da classe Alimento do banco de dados com o nome especificado.

    Args:
    nome (str): O nome do alimento a ser deletado.

    Returns:
    bool: Retorna True se o alimento foi deletado com sucesso do banco de dados, caso contrário, retorna False.
    """
     
    try:
        alimento = Alimento.select().where(Alimento.nome == nome).get()
        alimento.delete_instance()
        return True
    except:
        return False
