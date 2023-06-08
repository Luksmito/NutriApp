from fpdf import FPDF
from controllers.dieta_crud import *
from controllers.refeicao_crud import *


def gerar_pdf(dieta, caminho):
    pdf = FPDF()
    
    pdf.add_page()
    
    #Titulo
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 10, dieta.nome , 0, 1, "C")
    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 20, dieta.descricao, 0, 1, "C")
    pdf.set_font("Arial", "", 16)
    
    for refeicao in dieta.refeicoes:
        pdf.set_font("Arial", "", 18)
        pdf.cell(0,10,refeicao.nome, 1, 1, "L")
        texto = ''
        for alimento in ler_alimentos_refeicao(refeicao):
            texto += f"{alimento.alimento.nome}:   {alimento.quantidade}\n"
        pdf.set_font("Arial", "", 14)    
        pdf.multi_cell(0,10,texto, 0, 1, "L")
    
    pdf.output(f"{caminho}/{dieta.nome}.pdf")
