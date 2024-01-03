from pprint import pprint

from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
    select,
    text,
)
from sqlalchemy.orm import Session, declarative_base, relationship

Base = declarative_base()

# engine = create_engine('sqlite:///./desafio_sqlite_mongo_db/sqlite/desafio.db')
engine = create_engine('sqlite://')


class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(30))
    cpf = Column(String(11), unique=True)
    endereco = Column(String(50))

    conta = relationship('Conta', back_populates='cliente')

    def __repr__(self):
        return f'Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf}, endereco={self.endereco})'


class Conta(Base):
    __tablename__ = 'conta'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_de_conta = Column(
        String(30), nullable=False, default='Conta Corrente'
    )
    agencia = Column(String(10), nullable=False)
    numero = Column(Integer, unique=True)
    saldo = Column(Float, nullable=False)
    id_cliente = Column(Integer, ForeignKey('cliente.id'), nullable=False)

    cliente = relationship('Cliente', back_populates='conta')

    def __repr__(self):
        return (
            f'Conta(id={self.id}, tipo={self.tipo_de_conta}, agencia={self.agencia},'
            f'numero={self.numero}, saldo={self.saldo})'
        )


Base.metadata.create_all(engine)

# inspector_engine = inspect(engine)


with Session(engine) as session:
    carlos = Cliente(
        nome='Carlos Eduardo',
        cpf='01234567891',
        endereco='Rua Arthur Antunes 1981',
        conta=[
            Conta(
                tipo_de_conta='Conta Conrrente',
                agencia='0001',
                numero=9102,
                saldo=500.00,
            )
        ],
    )

    afonso = Cliente(
        nome='Afonso Henrique',
        cpf='33322211144',
        endereco='Rua Leandro 1982',
        conta=[
            Conta(
                tipo_de_conta='Conta Conrrente',
                agencia='0001',
                numero=1891,
                saldo=500.00,
            )
        ],
    )

    session.add_all([carlos, afonso])
    session.commit()

statement = select(Cliente).where(
    Cliente.nome.in_(['Carlos Eduardo', 'Afonso Henrique'])
)

for cliente in session.scalars(statement):
    print(cliente)

statement_join = select(Cliente.nome, Conta.numero).join_from(Conta, Cliente)

connection = engine.connect()
results = connection.execute(statement_join).fetchall()
for result in results:
    pprint(result)

statement_conta = select(Conta).where(Conta.id_cliente.in_([1, 2]))
print('\nRecuperando as contas')
for conta in session.scalars(statement_conta):
    print(conta)

print('\n Executando statement com sql')
sql = text('select * from cliente')

with engine.connect() as conn_sql:
    result = conn_sql.execute(sql)
    conn_sql.commit()

for row in result:
    print(row)
