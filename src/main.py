from fastapi import FastAPI
import uvicorn
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from src.api.hotels import router as router_hotels
from src.config import settings

app = FastAPI()

app.include_router(router_hotels)

@app.get("/", summary="Кто то забыл удалить ....")
def func():
    return "Hello world"

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)