from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.orm import Session

from src.data_module.settlement_data_module import get_db
from src.service_module.pedido_service import PedidoService
from src.data_module.models.produto import Produto
from src.templates_config import templates



router = APIRouter(prefix='/pedido')
 
@router.get('/')
def list_pedido(req: Request, db: Session = Depends(get_db)):
    
    pedidos = PedidoService.get_all(db)
    
    cxt = dict(pedidos=pedidos or [])
    return  templates.TemplateResponse(request=req, name='pedido/list_pedido.html', context=cxt)

@router.get('/{pedido_id}')
def get_pedido(req: Request, pedido_id: int = None, db: Session = Depends(get_db)):
    
    if pedido_id:
        
        pedido = PedidoService.get_pedido(db, pedido_id)
        
        if not pedido: return RedirectResponse(url=req.url_for('list_pedido'))
        
        cxt = dict(pedido=pedido)
        return  templates.TemplateResponse(request=req, name='pedido/get_pedido.html', context=cxt)
    
    return RedirectResponse(url=req.url_for('list_pedido'))

@router.post('/{produto_id}')
def novo_pedido(req: Request, produto_id: int = None, quantity: int = 1, pay_now: bool = False, db: Session = Depends(get_db)):
    
    if produto_id:
        
        produto = db.query(Produto).filter(Produto.id == produto_id).first()
        
        if not produto: return {"url": str( req.url_for('list_pedido')) }
        
        payment_link = PedidoService.create_pedido(db, produto, int(quantity))
        
        if payment_link is None: return {"url": str( req.url_for('list_pedido')) }
        
        if pay_now:
            return {"url": str(payment_link) }
           
    
    return {"url": str( req.url_for('list_pedido')) }


