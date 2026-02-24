from sqlalchemy import Column, Integer, String, ForeignKey, Table, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func 

import enum

from ..settlement_data_module import *

from .produto import Produto

pedido_produtos = Table(
    'pedido_produtos',
    Base.metadata,
    Column('pedido_id', Integer, ForeignKey('pedidos.id'), primary_key=True),
    Column('produto_id', Integer, ForeignKey('produtos.id'), primary_key=True)
)

class PedidoStatusEnum(enum.Enum):
    
    PENDENTE = "pendente"
    REJEITADO = "rejeitado"
    PAGO = "pago"
    CANCELADO = "cancelado"

class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Enum(PedidoStatusEnum), default=PedidoStatusEnum.PENDENTE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    preference_id = Column(String, index=True) # Para vincular a volta do usuário
    external_reference = Column(String, unique=True) # O seu ID de controle enviado ao MP
    payment_id = Column(String) # Preenchido somente após o pagamento
    merchant_order_id = Column(String)
    link_pagamento = Column(String) #init_point

    produtos = relationship('Produto', secondary=pedido_produtos, backref='pedidos')


Base.metadata.create_all(engine)