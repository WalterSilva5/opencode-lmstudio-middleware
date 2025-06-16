import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    LM_STUDIO_BASE_URL = os.environ.get("LM_STUDIO_BASE_URL")
    if LM_STUDIO_BASE_URL is None:
        print("\n\nAlerta: Variável de ambiente 'LM_STUDIO_BASE_URL' não está setada. Usando valor padrão 'http://localhost:1234'.")
        LM_STUDIO_BASE_URL = "http://localhost:1234"
    TIMEOUT = 60.0
    MODELS_TIMEOUT = 30.0
    HOST = "0.0.0.0"
    PORT = 8090

