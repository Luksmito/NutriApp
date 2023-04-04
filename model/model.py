from peewee import *
import os

DB_FILE = "nutriapp.db"  # nome do arquivo do banco de dados

# obtém o caminho absoluto do diretório do aplicativo
app_dir = os.path.dirname(os.path.abspath(__file__))

# cria o caminho completo para o arquivo do banco de dados
db_path = os.path.join(app_dir, DB_FILE)
db = SqliteDatabase(db_path)

class Alimento(Model):
    nome = CharField(max_length=25, unique=True)
    calorias_por_grama = FloatField(null=True)
    calorias_por_colher = FloatField(null=True)
    calorias_por_ml = FloatField(null=True)
    proteinas_por_grama = FloatField(null=True)
    carboidratos_por_grama = FloatField(null=True)
    gorduras_por_grama = FloatField(null=True)
    proteinas_por_colher = FloatField(null=True)
    carboidratos_por_colher = FloatField(null=True)
    gorduras_por_colher = FloatField(null=True)
    proteinas_por_ml = FloatField(null=True)
    carboidratos_por_ml = FloatField(null=True)
    gorduras_por_ml = FloatField(null=True)
    descricao = TextField(null=True)

    class Meta:
        database = db 

class Refeicao(Model):
    nome = CharField(max_length=40, unique=True)
    descricao = TextField(null=True)
    calorias_totais = FloatField(null=True)
    proteinas_totais = FloatField(null=True)
    gorduras_totais = FloatField(null=True)
    carboidratos_totais = FloatField(null=True)

    class Meta:
        database = db

class AlimentoRefeicao(Model):
    alimento = ForeignKeyField(model=Alimento, on_delete="CASCADE", on_update="CASCADE")
    refeicao = ForeignKeyField(model=Refeicao, on_delete="CASCADE", on_update="CASCADE")
    quantidade = CharField(null=True)

    class Meta: 
        database = db

class Dieta(Model):
    nome = CharField(max_length=40)
    descricao = TextField(null=True)
    refeicoes = ManyToManyField(model=Refeicao, backref='dietas', on_delete="CASCADE", on_update="CASCADE")
    calorias_totais = FloatField(null=True)
    proteinas_totais = FloatField(null=True)
    gorduras_totais = FloatField(null=True)
    carboidratos_totais = FloatField(null=True)

    class Meta:
        database = db

#RefeicaoDieta = Dieta.refeicoes.get_through_model()

#db.create_tables([Alimento, Refeicao, AlimentoRefeicao, Dieta, RefeicaoDieta])