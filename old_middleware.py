from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, Response
import httpx
import json
import asyncio

app = FastAPI()
LM_STUDIO_BASE_URL = "http://localhost:1234"

@app.post("/v1/chat/completions")
async def proxy(request: Request):
    body = await request.body()
    headers = dict(request.headers)
    
    filtered_headers = {k: v for k, v in headers.items() 
                       if k.lower() not in {'host', 'content-length'}}

    try:
        body_json = json.loads(body)
    except json.JSONDecodeError:
        return Response(content="Invalid JSON", status_code=400)

    # Remove tools/functions que podem causar problemas
    tools_removed = []
    if 'tools' in body_json:
        tools_removed.append('tools')
        del body_json['tools']
    if 'functions' in body_json:
        tools_removed.append('functions')
        del body_json['functions']
    if 'tool_choice' in body_json:
        tools_removed.append('tool_choice')
        del body_json['tool_choice']
    if 'function_call' in body_json:
        tools_removed.append('function_call')
        del body_json['function_call']
    
    if tools_removed:
        print(f"Removed from request: {', '.join(tools_removed)}")
    
    # Reconstrói o body sem as tools
    body = json.dumps(body_json).encode('utf-8')

    is_stream = body_json.get("stream", False)

    if is_stream:
        async def stream_generator():
            try:
                async with httpx.AsyncClient(timeout=60.0) as client:
                    async with client.stream(
                        "POST",
                        f"{LM_STUDIO_BASE_URL}/v1/chat/completions",
                        content=body,
                        headers=filtered_headers,
                    ) as response:
                        if response.status_code != 200:
                            error_content = ""
                            try:
                                error_content = await response.aread()
                                error_content = error_content.decode('utf-8')
                                print(f"Error response: {error_content}")
                            except:
                                pass
                            
                            error_msg = f'{{"error": "HTTP {response.status_code}: {error_content}"}}'
                            yield f"data: {error_msg}\n\n"
                            yield "data: [DONE]\n\n"
                            return
                        
                        # Processa o stream linha por linha
                        async for line in response.aiter_lines():
                            line = line.strip()
                            if line:
                                print(f"Line received: {line}")
                                
                                # Só processa linhas que começam com 'data:'
                                if line.startswith('data: '):
                                    data_content = line[6:]  # Remove 'data: '
                                    
                                    # Verifica se é [DONE]
                                    if data_content == '[DONE]':
                                        yield f"data: [DONE]\n\n"
                                        break
                                    
                                    # Verifica se é JSON válido
                                    try:
                                        json.loads(data_content)
                                        yield f"{line}\n\n"
                                    except json.JSONDecodeError:
                                        # Se não for JSON válido, cria uma resposta de erro válida
                                        error_response = {
                                            "error": {
                                                "message": data_content.strip('"'),
                                                "type": "context_length_exceeded",
                                                "code": "context_length_exceeded"
                                            }
                                        }
                                        yield f"data: {json.dumps(error_response)}\n\n"
                                        yield f"data: [DONE]\n\n"
                                        return
                                
                                # Ignora linhas 'event:' e outras que não sejam 'data:'
                        
            except Exception as e:
                print(f"Stream error: {e}")
                error_response = {
                    "error": {
                        "message": str(e),
                        "type": "stream_error",
                        "code": "stream_error"
                    }
                }
                yield f"data: {json.dumps(error_response)}\n\n"
            finally:
                yield f"data: [DONE]\n\n"

        return StreamingResponse(stream_generator(), media_type="text/event-stream")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            f"{LM_STUDIO_BASE_URL}/v1/chat/completions",
            content=body,
            headers=filtered_headers
        )
        excluded = {"content-encoding", "transfer-encoding", "content-length", "connection"}
        response_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded}
        return Response(content=resp.content, status_code=resp.status_code, headers=response_headers)


@app.get("/v1/models")
async def models_v1():
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(f"{LM_STUDIO_BASE_URL}/v1/models")
        excluded = {"content-encoding", "transfer-encoding", "content-length", "connection"}
        filtered_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded}
        return Response(content=resp.content, status_code=resp.status_code, headers=filtered_headers)

@app.get("/api/v0/models")
async def models_v0():
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(f"{LM_STUDIO_BASE_URL}/api/v0/models")
        excluded = {"content-encoding", "transfer-encoding", "content-length", "connection"}
        filtered_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded}
        return Response(content=resp.content, status_code=resp.status_code, headers=filtered_headers)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8090)
