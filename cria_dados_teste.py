import controllers.alimento_crud as alimento_controller
import controllers.refeicao_crud as refeicao_controller
import pandas as pd

def cria_alimentos():
    arroz = {
        'nome': 'Arroz',
        'calorias_por_grama': 3.5,
        'calorias_por_colher': None,
        'calorias_por_ml': None,
        'proteinas_por_grama': 0.6,
        'carboidratos_por_grama': 25.6,
        'gorduras_por_grama': 0.3,
        'proteinas_por_colher': None,
        'carboidratos_por_colher': None,
        'gorduras_por_colher': None,
        'proteinas_por_ml': None,
        'carboidratos_por_ml': None,
        'gorduras_por_ml': None,
        'descricao': 'Arroz branco cozido'
    }
    feijao = {
        'nome': 'Feijão',
        'calorias_por_grama': 1.2,
        'calorias_por_colher': None,
        'calorias_por_ml': None,
        'proteinas_por_grama': 0.7,
        'carboidratos_por_grama': 8.5,
        'gorduras_por_grama': 0.3,
        'proteinas_por_colher': None,
        'carboidratos_por_colher': None,
        'gorduras_por_colher': None,
        'proteinas_por_ml': None,
        'carboidratos_por_ml': None,
        'gorduras_por_ml': None,
        'descricao': 'Feijão preto cozido'
    }
    leite = {
        'nome': 'Leite',
        'calorias_por_grama': 0.6,
        'calorias_por_colher': None,
        'calorias_por_ml': 0.6,
        'proteinas_por_grama': 0.04,
        'carboidratos_por_grama': 0.05,
        'gorduras_por_grama': 0.03,
        'proteinas_por_colher': None,
        'carboidratos_por_colher': None,
        'gorduras_por_colher': None,
        'proteinas_por_ml': 0.04,
        'carboidratos_por_ml': 0.05,
        'gorduras_por_ml': 0.03,
        'descricao': 'Leite integral'
    }
    frango = {
        'nome': 'Frango',
        'calorias_por_grama': 2.2,
        'calorias_por_colher': None,
        'calorias_por_ml': None,
        'proteinas_por_grama': 0.27,
        'carboidratos_por_grama': 0,
        'gorduras_por_grama': 0.11,
        'proteinas_por_colher': None,
        'carboidratos_por_colher': None,
        'gorduras_por_colher': None,
        'proteinas_por_ml': None,
        'carboidratos_por_ml': None,
        'gorduras_por_ml': None,
        'descricao': 'Peito de frango cozido'
    }
    print("Arroz criado") if alimento_controller.criar_alimento(arroz) else print("Erro arroz")
    print("feijao criado") if alimento_controller.criar_alimento(feijao) else print("Erro feijao")
    print("leite criado") if alimento_controller.criar_alimento(leite) else print("Erro leite")
    print("frango criado") if alimento_controller.criar_alimento(frango) else print("Erro frango")


def cria_refeicao():
    almoco = {
        "nome": "Almoço",
        "descricao": "Refeição principal do dia",
        "calorias_totais": 500,
        "proteinas_totais": 20,
        "gorduras_totais": 25,
        "carboidratos_totais": 70
    }
    cafe_da_manha = {
        "nome": "Café da manhã",
        "descricao": "Refeição para iniciar o dia",
        "calorias_totais": 350,
        "proteinas_totais": 15,
        "gorduras_totais": 10,
        "carboidratos_totais": 50
    }
    jantar = {
        "nome": "Jantar",
        "descricao": "Refeição noturna",
        "calorias_totais": 450,
        "proteinas_totais": 18,
        "gorduras_totais": 20,
        "carboidratos_totais": 60
    }
    lanche_tarde = {
        "nome": "Lanche da tarde",
        "descricao": "Refeição leve para o meio da tarde",
        "calorias_totais": 200,
        "proteinas_totais": 8,
        "gorduras_totais": 5,
        "carboidratos_totais": 30
    }
    ceia = {
        "nome": "Ceia",
        "descricao": "Refeição antes de dormir",
        "calorias_totais": 300,
        "proteinas_totais": 10,
        "gorduras_totais": 15,
        "carboidratos_totais": 40
    }
    print("almoco criado") if refeicao_controller.criar_refeicao(almoco) else print("erro almoco")
    print("cafe_da_manha criado") if refeicao_controller.criar_refeicao(cafe_da_manha) else print("erro cafe_da_manha")
    print("jantar criado") if refeicao_controller.criar_refeicao(jantar) else print("erro jantar")
    print("lanche_tarde criado") if refeicao_controller.criar_refeicao(lanche_tarde) else print("erro lanche_tarde")
    print("ceia criado") if refeicao_controller.criar_refeicao(ceia) else print("erro ceia")


def add_alimento_aux(refeicao, alimento, quantidade):
    if refeicao_controller.add_alimento(refeicao_controller.ler_refeicao(refeicao), alimento_controller.ler_alimento(alimento), quantidade):
        print(f"Adicionado: {quantidade} de {alimento} a {refeicao}") 
    else: 
        print(f"Erro ao adicionar: {quantidade} de {alimento} a {refeicao}")
    

def exibe_informacoes_refeicao(refeicao_nome):
    refeicao = refeicao_controller.ler_refeicao(refeicao_nome)
    alimentos = refeicao_controller.ler_alimentos_refeicao(refeicao)

    alimentos = [alimento for alimento in alimentos]

    print(f"{refeicao.nome:=^50}")
    print(f"Calorias totais: {str(refeicao.calorias_totais):<50}")
    for alimento in alimentos:
        print(f"{alimento.alimento.nome}: {str(alimento.quantidade)}")



def popular_banco_de_dados():
    data = pd.read_excel("Taco.xlsx")
    #print(data.head())
    #exit()
    for _, serie in data.iterrows():
        alimento = {
            "nome": serie["Descrição do Alimento"].strip(),
            "calorias_por_ml": None,
            "calorias_por_colher": None,
            "calorias_por_grama": round(serie["Energia(kcal)"]/100,2) if type(serie["Energia(kcal)"]) == float else 0,
            "carboidratos_por_grama": round(serie["Carboidrato(g)"]/100,2) if type(serie["Carboidrato(g)"]) == float else 0,
            "gorduras_por_grama": round(serie["Lipídeos(g)"]/100,2) if type(serie["Lipídeos(g)"]) == float else 0,
            "proteinas_por_grama": round(serie["Proteína(g)"]/100,2) if type(serie["Proteína(g)"]) == float else 0,
            "carboidratos_por_colher": None,
            "proteinas_por_colher": None,
            "gorduras_por_colher": None,
            "carboidratos_por_ml": None,
            "gorduras_por_ml": None,
            "proteinas_por_ml": None,
            "descricao": None
        }
        print(f"Alimento: {alimento['nome']}: ",alimento_controller.criar_alimento(alimento))




popular_banco_de_dados()




