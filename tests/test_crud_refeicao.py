import pytest
import sys
sys.path.append("/home/mrbushido/Documentos/programacao/NutriApp")
from model.model import Refeicao, Alimento
from controllers.refeicao_crud import criar_refeicao, ler_refeicoes, ler_refeicao, atualizar_refeicao, deletar_refeicao, add_alimento


def criar_alimento():
    """
    Cria um alimento no banco de dados para ser usado nos testes.

    Returns:
        Alimento: Um objeto Alimento representando o alimento criado.
    """
    return Alimento.create(nome="Arroz", calorias_por_grama=100)

def test_criar_refeicao():
    refeicao = {"nome": "Almoço", "descricao": "Refeição principal do dia"}
    assert criar_refeicao(refeicao) == True

def test_criar_refeicao_falha():
    
    # Tentativa de criar refeição sem o campo "nome"
    refeicao = {"descricao": "Almoço"}
    assert criar_refeicao(refeicao) == False

def test_ler_refeicoes():
    refeicao1 = {
        "nome" : "Cafe da manha",
        "descricao": "Refeicao matinal"
    }
    refeicao2 = {
        "nome" : "Jantar",
        "descricao": "Refeicao noturna"
    }
    # Cria duas refeições no banco de dados
    refeicao1 = criar_refeicao(refeicao1)
    refeicao2 = criar_refeicao(refeicao2)

    # Lê as refeições criadas
    refeicoes = ler_refeicoes()
    refeicoes = [refeicao for refeicao in refeicoes] 
    assert len(refeicoes) == 3
    assert refeicoes[0].nome == "Almoço"
    assert refeicoes[1].nome == "Cafe da manha"
    assert refeicoes[2].nome == "Jantar"

def test_ler_refeicao():
    

    # Lê a refeição criada
    refeicao_lida = ler_refeicao("Almoço")

    assert refeicao_lida is not None
    assert refeicao_lida.nome == "Almoço"

def test_atualizar_refeicao():
   

    # Atualiza a descrição da refeição criada
    refeicao_atualizada = {"descricao": "Segunda Refeição mais importante do dia"}
    assert atualizar_refeicao("Almoço", refeicao_atualizada) == True

    # Lê a refeição atualizada
    refeicao_lida = ler_refeicao("Almoço")

    assert refeicao_lida is not None
    assert refeicao_lida.descricao == "Segunda Refeição mais importante do dia"

