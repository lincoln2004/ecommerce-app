from src.data_module.models.produto import Produto, ProdutoImg
from src.service_module.upload_service import DriveUploadService

from sqlalchemy.orm import Session

from fastapi import UploadFile, HTTPException


class ProdutoService:
    
    @staticmethod
    def add_produto(db: Session, nome, preco, img: UploadFile, file_service: DriveUploadService):
        
        if not nome or not preco or not img or not file_service: return 
        
        file_id = None
        
        try:
            
            file_id = file_service.upload_file(img)
            
            if not file_id: return    
            
            temp_produto = Produto(nome=nome, preco=float(preco))
            db.add(temp_produto)
            db.flush()
            
            produto_img = ProdutoImg(produto_id=temp_produto.id, filename=img.filename, file_id= file_id)
            db.add(produto_img)
            
            db.commit()
            db.refresh(temp_produto)
            
            return temp_produto
        except Exception as e:
            print(e)
            db.rollback()   
            
            if file_id:
                file_service.delete_file(file_id) 
            
            raise HTTPException(status_code=500)
    
    @staticmethod            
    def remove_produto(db: Session, produto_id: int, file_service: DriveUploadService):
        
        if not db or not produto_id: return 
        
        produto = db.query(Produto).filter(Produto.id == produto_id).first()

        if produto:
            
            try:
                file_service.delete_file(produto.file_id)
            except Exception as e:
                print(e)
                raise HTTPException(status_code=500)
            
            try:
                db.delete(produto) 
                db.commit()      
            except:
                db.rollback()     
                
    @staticmethod
    def get_all(db: Session):

        try:
            return  db.query(Produto).all() or []
        except Exception as e: 
            print(e)
            return []          
    
    @staticmethod            
    def get_produto(db: Session, produto_id):
        
        if not db or not produto_id: return
        
        produto = db.query(Produto).filter(Produto.id == produto_id).first()

        if produto: return produto 
        return    
    
    @staticmethod            
    def get_img(db: Session, produto_id, file_service: DriveUploadService):
        
        if not db or not produto_id: return
        
        produto = db.query(Produto).filter(Produto.id == produto_id).first()

        if produto: 
            img = db.query(ProdutoImg).filter(ProdutoImg.produto == produto).first()
            if img: 
                
                img = file_service.get_file(img.file_id)
                
                if img: return img 
            
        return   
    
             