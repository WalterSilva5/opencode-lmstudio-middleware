from typing import AsyncGenerator
import httpx
import json
from utils import create_error_response, format_sse_line, is_valid_json
from config import Config

async def handle_error_response(response: httpx.Response) -> AsyncGenerator[str, None]:
    try:
        error_content = await response.aread()
        error_text = error_content.decode('utf-8')
        print(f"Error response: {error_text}")
    except:
        error_text = f"HTTP {response.status_code}"
    
    error_response = create_error_response(f"HTTP {response.status_code}: {error_text}")
    yield format_sse_line(json.dumps(error_response))
    yield format_sse_line("[DONE]")

async def process_stream_line(line: str) -> AsyncGenerator[str, None]:
    if not line.startswith('data: '):
        return
    
    data_content = line[6:]
    
    if data_content == '[DONE]':
        yield format_sse_line("[DONE]")
        return
    
    if is_valid_json(data_content):
        yield f"{line}\n\n"
    else:
        error_response = create_error_response(
            data_content.strip('"'),
            "context_length_exceeded",
            "context_length_exceeded"
        )
        yield format_sse_line(json.dumps(error_response))
        yield format_sse_line("[DONE]")

async def create_stream_generator(body: bytes, headers: dict) -> AsyncGenerator[str, None]:
    try:
        async with httpx.AsyncClient(timeout=Config.TIMEOUT) as client:
            async with client.stream(
                "POST",
                f"{Config.LM_STUDIO_BASE_URL}/v1/chat/completions",
                content=body,
                headers=headers,
            ) as response:
                
                if response.status_code != 200:
                    async for chunk in handle_error_response(response):
                        yield chunk
                    return
                
                async for line in response.aiter_lines():
                    line = line.strip()
                    if line:
                        print(f"Line received: {line}")
                        async for processed_line in process_stream_line(line):
                            yield processed_line
                            if "[DONE]" in processed_line:
                                return
    
    except Exception as e:
        print(f"Stream error: {e}")
        error_response = create_error_response(str(e), "stream_error", "stream_error")
        yield format_sse_line(json.dumps(error_response))
    finally:
        yield format_sse_line("[DONE]")
