from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.data_module.settlement_data_module import get_db

from dotenv import load_dotenv
load_dotenv()

import os 
import requests

from src.data_module.models.pedido import Pedido, PedidoStatusEnum

router = APIRouter()

import hmac
import hashlib

def verify_mp_signature(x_request_id, x_signature, resource_id, secret_key):
    
    if not x_signature or not resource_id or not secret_key:
        return False
    try:
        # 1. Separar o ts e o v1 do header x-signature
        # Exemplo de header: "ts=123456789,v1=f6e8..."
        parts = {part.split('=')[0]: part.split('=')[1] for part in x_signature.split(',')}
        ts = parts.get('ts')
        v1_received = parts.get('v1')

        # 2. Montar o "manifesto" (a string que será validada)
        # O formato exigido pelo Mercado Pago é: "id:[ID];request-id:[TS];"
        manifest = f"id:{resource_id};request-id:{x_request_id};ts:{ts};"

        # 3. Gerar o HMAC SHA256 usando sua Secret Key
        hmac_obj = hmac.HMAC(
            secret_key.encode('utf-8'), 
            manifest.encode('utf-8'), 
            hashlib.sha256
        )
        signature_generated = hmac_obj.hexdigest()

        # 4. Comparar as assinaturas
        return hmac.compare_digest(signature_generated, v1_received)
        
    except Exception as e:
        print(f"Erro na validação: {e}")
        return False

@router.post('/webhook')
async def webhook(req: Request, db: Session = Depends(get_db)):
    try:
        data = await req.json()
    except Exception:
        return JSONResponse(content={"status": "error"}, status_code=400)
    
    type_event = data.get('type') or req.query_params.get('topic')
    
    # O MP envia o ID dentro de 'data', mas às vezes o campo pode variar 
    # dependendo da versão da API. O padrão atual é este:
    if type_event in ('payment', 'merchant_order'):
        
        
        id_pagamento = data.get('data', {}).get('id') or req.query_params.get('data.id') or req.query_params.get('id')
        signature = req.headers.get('x-signature')
        x_request_id = req.headers.get('x-request-id')
    
        if not verify_mp_signature(x_request_id, signature, id_pagamento, os.environ.get('MP_WEBHOOK_SIGNATURE')):
            return JSONResponse(content={"status": "error"}, status_code=400)
        
        if not id_pagamento:
            return {"status": "ignored", "reason": "no id found"}

        # Consulta na API do Mercado Pago
        headers = {"Authorization": f"Bearer {os.getenv('MP_ACCESS_TOKEN')}"}
        url = f"https://api.mercadopago.com/v1/payments/{id_pagamento}"
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                payment_info = response.json()
                
                # O external_reference que você definiu na criação do pedido
                pedido_id = payment_info.get("external_reference")
                status_pagamento = payment_info.get("status")

                if pedido_id:
                    # Busca o pedido no banco
                    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
                    
                    if pedido:
                        # Evita atualizar se o pedido já estiver pago (Idempotência)
                        if pedido.status == PedidoStatusEnum.PAGO:
                            return {"status": "already_processed"}

                        if status_pagamento == "approved":
                            pedido.status = PedidoStatusEnum.PAGO
                            pedido.preference_id = None 
                            pedido.link_pagamento = None
                        elif status_pagamento in ["rejected", "cancelled"]:
                            pedido.status = PedidoStatusEnum.REJEITADO
                        
                        db.commit()
                        print(f"Pedido {pedido_id} atualizado para {status_pagamento}")
            
        except Exception as e:
            db.rollback()
            print(f"Erro ao consultar MP: {e}")
            return JSONResponse(content={"status": "error"}, status_code=500)

    # OBRIGATÓRIO: Retornar 200 ou 201 para o MP não reenviar a notificação infinitamente
    return {"status": "ok"}