from src.data_module.models.pedido import Pedido, PedidoStatusEnum
from src.data_module.models.produto import Produto

from sqlalchemy.orm import Session

from dotenv import load_dotenv
import os
import requests

load_dotenv()

class PedidoService:
    
    @staticmethod
    def create_pedido(db: Session, produto: Produto, quantity: int = 1):
        if not isinstance(produto, Produto):
            return None 
        
        try:
            pedido = Pedido()
            
            db.add(pedido)
            db.flush()
            
            pedido_id = str(pedido.id)
        
            # 1. Configurações de URL e Headers
            ACCESS_TOKEN = os.getenv('MP_ACCESS_TOKEN')
            TN_URL = f'https://{os.getenv("TN_URL")}'
            
            headers = {
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }
            
            # 2. Montagem do corpo (seu dicionário preferences)
            preferences = {
                "payer": {"email": os.getenv('TEST_EMAIL')},
                "notification_url": f"{TN_URL}/webhook",
                "back_urls": {
                    "success": f"{TN_URL}/success",
                    "pending": f"{TN_URL}/pending",
                    "failure": f"{TN_URL}/failure"
                },
                "payment_methods": {
                    "installments": 1
                },
                "items": [produto.preference_formated(quantity)],
                "external_reference": pedido_id,
                "auto_return": "approved"
            }
        
        
            # 3. Envio para o Mercado Pago
            response = requests.post(
                "https://api.mercadopago.com/checkout/preferences",
                json=preferences,
                headers=headers
            )
            
            response.raise_for_status() # Gera erro se a requisição falhar
            
            data = response.json()
            
            pedido.preference_id = data['id']  # preference_id
            pedido.link_pagamento = data['sandbox_init_point']
            pedido.external_reference = data["external_reference"]
            db.commit()
            
            print(data)
            return data['sandbox_init_point']
        except Exception as e:
            
            print(e)
            db.rollback()
            
            return None
        
    @staticmethod    
    def get_pedido(db: Session, pedido_id: str):
        
        if not pedido_id: return 
        
        try:
            return  db.query(Pedido).filter( Pedido.id == int(pedido_id)).first()
        except:
            return
        
    @staticmethod    
    def get_all(db: Session):
        
        try:
            return  db.query(Pedido).all() or []
        except: 
            return []
    
    @staticmethod    
    def pagar_pedido(db: Session, pedido_id: str, status: str):    
        
        if not pedido_id or not isinstance(pedido_id, (str,int)) or not status or not isinstance(status, str): return 
        
        pedido = PedidoService.get_pedido(db, int(pedido_id))
        
        if not pedido: return 
        
        if status == 'approved':
            pedido.status = PedidoStatusEnum.PAGO
            db.commit()
            return True
        
        return 