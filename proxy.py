import httpx
from fastapi.responses import Response
from .utils import filter_headers, filter_response_headers
from .config import Config

async def handle_non_stream_request(body: bytes, headers: dict) -> Response:
    async with httpx.AsyncClient(timeout=Config.TIMEOUT) as client:
        resp = await client.post(
            f"{Config.LM_STUDIO_BASE_URL}/v1/chat/completions",
            content=body,
            headers=headers
        )
        response_headers = filter_headers(dict(resp.headers))
        final_headers = filter_response_headers(response_headers)
        
        return Response(
            content=resp.content, 
            status_code=resp.status_code, 
            headers=final_headers
        )

async def proxy_models_endpoint(endpoint: str) -> Response:
    async with httpx.AsyncClient(timeout=Config.MODELS_TIMEOUT) as client:
        resp = await client.get(f"{Config.LM_STUDIO_BASE_URL}{endpoint}")
        response_headers = filter_headers(dict(resp.headers))
        final_headers = filter_response_headers(response_headers)
        
        return Response(
            content=resp.content, 
            status_code=resp.status_code, 
            headers=final_headers
        )
