import pytest
import sys

sys.path.append("/home/mrbushido/Documentos/programacao/NutriApp")

from controllers import alimento_crud

def test_criar_alimento():
    alimento = {
        'nome': 'Arroz',
        'calorias_por_grama': 1.2,
        'calorias_por_colher': 25,
        'calorias_por_ml': None,
        'proteinas_por_grama': 0.2,
        'carboidratos_por_grama': 2.2,
        'gorduras_por_grama': 0.1,
        'descricao': 'Alimento rico em carboidratos.'
    }
    assert alimento_crud.criar_alimento(alimento) == True

def test_ler_alimentos():
    assert alimento_crud.ler_alimentos() is not None

def test_ler_alimento():
    assert alimento_crud.ler_alimento('Arroz') is not None

def test_atualizar_alimento():
    alimento_atualizado = {
        'calorias_por_grama': 1.5,
        'calorias_por_colher': 30,
        'proteinas_por_grama': 0.3
    }
    assert alimento_crud.atualizar_alimento('Arroz', alimento_atualizado) == True

def test_deletar_alimento():
    assert alimento_crud.deletar_alimento('Arroz') == True


