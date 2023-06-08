from playhouse.sqlite_ext import SqliteExtDatabase
from unidecode import unidecode
db = SqliteExtDatabase('nutriapp.db')

@db.func()
def retirar_acentos(texto):
    return unidecode(texto)
    
