import uvicorn
from app import create_app
from config import Config

if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)
