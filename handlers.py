from fastapi import Request
from fastapi.responses import StreamingResponse, Response
import json
from .utils import filter_headers, remove_tool_calls
from .streaming import create_stream_generator
from .proxy import handle_non_stream_request, proxy_models_endpoint

async def chat_completions(request: Request):
    body = await request.body()
    headers = filter_headers(dict(request.headers))

    try:
        body_json = json.loads(body)
    except json.JSONDecodeError:
        return Response(content="Invalid JSON", status_code=400)

    body_json, tools_removed = remove_tool_calls(body_json)
    if tools_removed:
        print(f"Removed from request: {', '.join(tools_removed)}")

    body = json.dumps(body_json).encode('utf-8')
    is_stream = body_json.get("stream", False)

    if is_stream:
        return StreamingResponse(
            create_stream_generator(body, headers), 
            media_type="text/event-stream"
        )
    else:
        return await handle_non_stream_request(body, headers)

async def models_v1():
    return await proxy_models_endpoint("/v1/models")

async def models_v0():
    return await proxy_models_endpoint("/api/v0/models")
