from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

from pathlib import Path
from starlette import status

from src.controller_module.products_controller import router as product_controller
from src.controller_module.webhook_controller import router as webhook_controller
from src.controller_module.pedidos_controller import router as pedidos_controller
from src.controller_module.backurls_controller import router as backurls_controller

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, use os domínios do Mercado Pago
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent.parent

app.mount('/static', StaticFiles(directory= BASE_DIR / 'static'), name='static')

@app.exception_handler(Exception)
async def global_exception_handler(exc: Exception):
    # 1. Verifica se o erro já tem um status definido (erros que você deu 'raise')
    if isinstance(exc, HTTPException):
        status_code = exc.status_code
    else:
        # 2. Se for um bug inesperado (divisão por zero, erro de banco, etc)
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = "An error occurred while processing the request. Try again later."

    if status_code == status.HTTP_404_NOT_FOUND:
        message = "Page not found"
    elif status_code == status.HTTP_400_BAD_REQUEST:
        message = "We couldn't process that request"
    elif status_code == status.HTTP_401_UNAUTHORIZED:
        message = "Unauthorized access"       
        
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message
        },
    )
    
app.include_router(product_controller) 
app.include_router(webhook_controller)   
app.include_router(pedidos_controller)   
app.include_router(backurls_controller)   

@app.get('/')
def main(req: Request):
    return RedirectResponse(url=req.url_for('list_produto'), status_code=303)