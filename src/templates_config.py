from pathlib import Path 
from fastapi.templating import Jinja2Templates

from datetime import datetime

BASE_DIR = Path(__file__).parent.parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def format_datetime(value):
    if not value: return ""
    if isinstance(value, str):
        # Converte string para objeto
        value = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return value.strftime('%d/%m/%Y')

templates.env.filters["date_format"] = format_datetime