from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from ..settlement_data_module import *

class Produto(Base):
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, default=0.0, nullable=False)
    
    imagem = relationship("ProdutoImg", backref="produto", cascade="all, delete-orphan", uselist=False)
    
    def preference_formated(self, quantity: int = 1):
        
        return {
            "id": self.id,
            "title": self.nome,
            "quantity": quantity,
            "unit_price": self.preco,
            "currency_id": "BRL"
        }

class ProdutoImg(Base):
    __tablename__ = 'produto_img'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False, unique=True)
    file_id = Column(String, nullable=False)
    produto_id = Column(Integer, ForeignKey('produtos.id'), unique=True)

Base.metadata.create_all(engine)