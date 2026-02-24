from fastapi import APIRouter, Request

from dotenv import load_dotenv
load_dotenv()

from src.templates_config import templates

router = APIRouter()

@router.get('/success')
def success_url(req: Request):
    
    return templates.TemplateResponse(req, 'backurls/success.html')

@router.get('/pending')
def pending_url(req: Request):
    
    return templates.TemplateResponse(req, 'backurls/pending.html')

@router.get('/failure')
def failure_url(req: Request):
    
    return templates.TemplateResponse(req, 'backurls/failure.html')