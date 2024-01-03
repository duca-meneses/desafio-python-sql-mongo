from os import environ
from pprint import pprint

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient

load_dotenv()

uri = environ['MONGO_DB_URI']

client = MongoClient(uri)

db = client.test
collection = db.test_collection

print(db.test_collection)

post = {
    'nome': 'Carlos Eduardo',
    'cpf': '01234567891',
    'endereco': 'Rua Arthur Antunes',
    'conta': {
        'tipo': 'Conta Corrente',
        'agencia': '0001',
        'numero': 9102,
        'saldo': 500.00,
    },
}

posts = db.posts
# post_id = posts.insert_one(post).inserted_id
# print(post_id)

pprint(db.posts.find_one())

new_posts = [
    {
        'nome': 'Afonso Henrique',
        'cpf': '11122233344',
        'endereco': 'Rua leandro 1982',
        'conta': {
            'tipo': 'Conta Poupança',
            'agencia': '0001',
            'numero': 1891,
            'saldo': 1500.00,
        },
    },
    {
        'nome': 'John Smith',
        'cpf': '12341234123',
        'endereco': 'Rua leandro 1982',
        'conta': {
            'tipo': 'Conta Conrrent',
            'agencia': '0001',
            'numero': 2891,
            'saldo': 10500.00,
        },
    },
]

result = posts.insert_many(new_posts)
print(result.inserted_ids)

print('\n Documentos presente na coleção')
for post in posts.find():
    pprint(post)
