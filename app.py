from fastapi import FastAPI
from handlers import chat_completions, models_v1, models_v0

def create_app() -> FastAPI:
    app = FastAPI()
    
    app.post("/v1/chat/completions")(chat_completions)
    app.get("/v1/models")(models_v1)
    app.get("/api/v0/models")(models_v0)
    
    return app
