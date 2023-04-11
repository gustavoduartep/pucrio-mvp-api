from sqlalchemy import Column, String, Integer, DateTime, Float
from datetime import datetime
from typing import Union

from model.base import Base

class Item(Base):
    __tablename__ = 'item'

    id = Column("pk_item", Integer, primary_key=True)
    nome = Column(String(80), unique=True)
    quantidade = Column(Integer)
    valor = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, nome:str, quantidade:int, valor:float, data_criacao:Union[DateTime, None] = None):
        """
        Cria um novo Item

        Arguments:
            nome: Nome do item ou peça
            quantidade: Quantidade de itens do pedido
            valor: Valor unitário do item
            data_criacao: Data de cadastro do produto
        """

        self.nome = nome
        self.quantidade = quantidade
        self.valor = valor
        
        if data_criacao:
            self.data_criacao = data_criacao
