import sys
sys.path.append("../")
from model.model import Refeicao, AlimentoRefeicao, Alimento

def criar_refeicao(refeicao):
    """
    Cria uma nova refeição no banco de dados.

    Args:
        refeicao (dict): Um dicionário contendo informações sobre a refeição.
            Deve conter as chaves 'nome' e 'descricao'.

    Returns:
        bool: True se a refeição foi criada com sucesso, False caso contrário.

    """
    try:
        Refeicao.create(
            nome=refeicao["nome"],
            descricao=refeicao["descricao"]
        )
        return True
    except:
        return False

def ler_refeicoes():
    """
    Lê todas as refeições no banco de dados.

    Returns:
        list: Uma lista de objetos Refeicao representando todas as refeições no banco de dados,
            ou None se ocorreu um erro ao acessar o banco de dados.
    """

    try:
        refeicoes = Refeicao.select()
        return refeicoes
    except:
        return None

def ler_refeicao(nome):
    """
    Lê uma refeição específica no banco de dados.

    Args:
        nome (str): O nome da refeição que deve ser lida.

    Returns:
        Refeicao: Um objeto Refeicao representando a refeição com o nome especificado,
            ou None se a refeição não pôde ser encontrada ou ocorreu um erro ao acessar o banco de dados.
    """

    try:
        refeicao = Refeicao.select().where(Refeicao.nome == nome).get()
        return refeicao
    except:
        return None

def atualizar_refeicao(nome, refeicao):
    """
    Atualiza as informações de uma refeição no banco de dados.

    Args:
        nome (str): O nome da refeição que deve ser atualizada.
        refeicao (dict): Um dicionário contendo informações atualizadas sobre a refeição.
            Pode conter algumas ou todas as chaves que o dicionário de criação de refeições tem.

    Returns:
        bool: True se a refeição foi atualizada com sucesso, False caso contrário.
    """
    try:
        campos = refeicao.keys()
        refeicao_buscada = ler_refeicao(nome)
        if "nome" in  campos:
            refeicao_buscada.nome = refeicao["nome"]
        if "descricao" in campos:
            refeicao_buscada.descricao = refeicao["descricao"]
        if "calorias_totais" in campos:
            refeicao_buscada.calorias_totais = refeicao["calorias_totais"]
        if "proteinas_totais" in campos:
            refeicao_buscada.proteinas_totais = refeicao["proteinas_totais"]
        if "gorduras_totais" in campos:
            refeicao_buscada.gorduras_totais = refeicao["gorduras_totais"]
        if "carboidratos_totais" in campos:
            refeicao_buscada.carboidratos_totais = refeicao["carboidratos_totais"]    
        refeicao_buscada.save()
        return True
    except Exception as e:
        print(f"{e}")
        return False

def deletar_refeicao(nome):
    """
    Deleta um objeto da classe Refeicao do banco de dados com o nome especificado.

    Args:
    nome (str): O nome da refeição a ser deletada.

    Returns:
    bool: Retorna True se a refeição foi deletada com sucesso do banco de dados, caso contrário, retorna False.
    """
     
    try:
        refeicao = Refeicao.select().where(Refeicao.nome == nome).get()
        refeicao.delete_instance()
        return True
    except:
        return False

def add_alimento(refeicao, alimento, quantidade=None):
    """
    Adiciona um alimento em uma refeição, falando em banco de dados, cria uma nova linha na tabela de relação ManyToMany

    Args:
    refeicao (Model): Objeto da refeicao que será adicionado o alimento
    alimento (Model): Objeto do alimento que será adicionado a refeição

    Returns:
    bool: Retorna True se o alimento foi criado com sucesso, caso contrário, retorna False
    """

    try:
        AlimentoRefeicao.create(refeicao=refeicao.id, alimento=alimento.id, quantidade=quantidade)
        return True
    except Exception as e:
        print(f"{e}")
        return False

def remove_alimento(refeicao, alimento):
    """
    Remove um alimento de uma refeição, falando em banco de dados, deleta uma linha na tabela de relação ManyToMany

    Args:
    refeicao (Model): Objeto da refeicao que será deletado o alimento
    alimento (Model): Objeto do alimento que será deletado da refeição

    Returns:
    bool: Retorna True se o alimento foi deletado com sucesso, caso contrário, retorna False
    """
    try:
        alimentos = AlimentoRefeicao.select().where(AlimentoRefeicao.refeicao == refeicao.id and AlimentoRefeicao.alimento == alimento.id).get()
        alimentos.delete_instance()
        return True
    except Exception as e:
        print(f"{e}")
        return False

def ler_alimentos_refeicao(refeicao):
    """
    Le os alimentos relacionados com a refeicao
    Args:

    refeicao (Model): Objeto da refeicao que será lida

    Returns:
    bool: Retorna as linhas da relacao se encontrado, caso contrário, retorna None
    """
    try:
        alimentos = AlimentoRefeicao.select().where(AlimentoRefeicao.refeicao == refeicao)
        return alimentos
    except:
        return None

def processa_quantidade(quantidade):
    numero = ''
    for i in quantidade:
        if i.isdigit() or i == ".":
            numero += i
        else:
            break
    
    return (float(numero),quantidade[len(quantidade)-2]+quantidade[len(quantidade)-1])

def calcula_informacoes_nutricionais(refeicao):

    try:
        alimentos = AlimentoRefeicao.select().where(AlimentoRefeicao.refeicao == refeicao.id)
        refeicao_atualizada = {
            "calorias_totais": 0,
            "gorduras_totais": 0,
            "proteinas_totais": 0,
            "carboidratos_totais": 0
        }

        for alimento in alimentos:
            quantidade = processa_quantidade(alimento.quantidade)
    
            #Calcula a quantidade de calorias
            if quantidade[1] == 'gr':
                refeicao_atualizada["calorias_totais"] += quantidade[0]*alimento.alimento.calorias_por_grama
            elif quantidade[1] == 'ml':
                refeicao_atualizada["calorias_totais"] += quantidade[0]*alimento.alimento.calorias_por_ml
            elif quantidade[1] == 'cl':
                refeicao_atualizada["calorias_totais"] += quantidade[0]*alimento.alimento.calorias_por_colher
            
            #Calcula a quantidade de gordura
            if alimento.alimento.gorduras_por_grama is not None and quantidade[1] == 'gr':
                refeicao_atualizada["gorduras_totais"] += alimento.alimento.gorduras_por_grama*quantidade[0]
            elif alimento.alimento.gorduras_por_colher is not None and quantidade[1] == 'cl':
                refeicao_atualizada["gorduras_totais"] += alimento.alimento.gorduras_por_colher*quantidade[0]
            elif alimento.alimento.gorduras_por_ml is not None and quantidade[1] == 'ml':
                refeicao_atualizada["gorduras_totais"] += alimento.alimento.gorduras_por_ml*quantidade[0]
            
            #Calcula a quantidade de carboídratos
            if alimento.alimento.carboidratos_por_grama is not None and quantidade[1] == 'gr':
                refeicao_atualizada["carboidratos_totais"] += alimento.alimento.carboidratos_por_grama*quantidade[0]
            elif alimento.alimento.carboidratos_por_colher is not None and quantidade[1] == 'cl':
                refeicao_atualizada["carboidratos_totais"] += alimento.alimento.carboidratos_por_colher*quantidade[0]
            elif alimento.alimento.carboidratos_por_ml is not None and quantidade[1] == 'ml':
                refeicao_atualizada["carboidratos_totais"] += alimento.alimento.carboidratos_por_ml*quantidade[0]
            
            if alimento.alimento.proteinas_por_grama is not None and quantidade[1] == 'gr':
                refeicao_atualizada["proteinas_totais"] += alimento.alimento.proteinas_por_grama*quantidade[0]
            elif alimento.alimento.proteinas_por_colher is not None and quantidade[1] == 'cl':
                refeicao_atualizada["proteinas_totais"] += alimento.alimento.proteinas_por_colher*quantidade[0]
            elif alimento.alimento.proteinas_por_ml is not None and quantidade[1] == 'ml':
                refeicao_atualizada["proteinas_totais"] += alimento.alimento.proteinas_por_ml*quantidade[0]
        
        atualizar_refeicao(refeicao.nome, refeicao_atualizada)
        return True
    except Exception as e:
        print(f"Erro: {e}")
        return False