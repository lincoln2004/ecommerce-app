from fastapi import APIRouter, Depends, Request, HTTPException, File, UploadFile, Form
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session 
from pydantic import BaseModel, Field, ValidationError

from src.data_module.settlement_data_module import get_db
from src.service_module.produto_service import ProdutoService
from src.service_module.upload_service import DriveUploadService
from src.templates_config import templates

router = APIRouter(prefix='/produto')

@router.get('/')
async def list_produto(req: Request, db: Session = Depends(get_db)):
    
    produtos = ProdutoService.get_all(db)
    
    if produtos:    
        cxt = dict(produtos=produtos)
        return  templates.TemplateResponse(request=req, name='produto/list_produto.html', context=cxt)

    return  templates.TemplateResponse(request=req, name='produto/list_produto.html')

@router.get('/{produto_id}')
async def get_produto(req: Request, produto_id: int, db: Session = Depends(get_db)):
    
    produto = ProdutoService.get_produto(db, produto_id)
    
    if produto:
        cxt = dict(produto=produto)
        return  templates.TemplateResponse(request=req, name='produto/get_produto.html', context=cxt)
    
    raise HTTPException(status_code=400)

@router.get('/img/{produto_id}')
async def get_img(produto_id: int, db: Session = Depends(get_db)):
    
    produto = ProdutoService.get_produto(db, produto_id)
    
    if produto:
        img = ProdutoService.get_img(db, produto.id, DriveUploadService())
        
        return RedirectResponse(url=img)
        
    return {"error": "Image not found"}    
    
class ProdutoValidator(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    preco: float = Field(..., gt=0)

@router.post('/add')
async def add_produto(nome: str = Form(...), preco: float = Form(...), image: UploadFile = File(...), db: Session = Depends(get_db)):
    
    try:
        validated_data = ProdutoValidator(nome=nome, preco=preco)
    except ValidationError as e:
        # Se os dados estiverem errados, lança erro 400 (Bad Request)
        raise HTTPException(status_code=400, detail=e.errors())

    allowed_contenttype = ["image/jpeg", "image/png", "image/webp"]
    
    if image.content_type in allowed_contenttype:
        
        produto = ProdutoService.add_produto(db, validated_data.nome, validated_data.preco, image, DriveUploadService())
        
        if not produto: raise HTTPException(status_code=500) 
    
        return produto
    
    raise HTTPException(status_code=400)

@router.delete('/delete/{produto_id}')
async def delete_produto(req: Request, produto_id: str, db: Session = Depends(get_db)):
    
    if not produto_id or not isinstance(produto_id, int):
        raise HTTPException(status_code=400)
    
    produto = ProdutoService.get_produto(db, produto_id)
    
    if produto:
        ProdutoService.remove_produto(db, produto.id, DriveUploadService())
        
    return RedirectResponse(req.url_for('list_produto'), status_code= 303)