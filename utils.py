from typing import Dict, Tuple
import json

def filter_headers(headers: Dict[str, str]) -> Dict[str, str]:
    excluded = {'host', 'content-length'}
    return {k: v for k, v in headers.items() if k.lower() not in excluded}

def remove_tool_calls(body_json: dict) -> Tuple[dict, list]:
    tools_removed = []
    tool_fields = ['tools', 'functions', 'tool_choice', 'function_call']
    
    for field in tool_fields:
        if field in body_json:
            tools_removed.append(field)
            del body_json[field]
    
    return body_json, tools_removed

def create_error_response(message: str, error_type: str = "error", code: str = "error") -> dict:
    return {
        "error": {
            "message": message,
            "type": error_type,
            "code": code
        }
    }

def format_sse_line(content: str) -> str:
    return f"data: {content}\n\n"

def is_valid_json(text: str) -> bool:
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False

def filter_response_headers(headers: dict) -> dict:
    excluded = {"content-encoding", "transfer-encoding", "content-length", "connection"}
    return {k: v for k, v in headers.items() if k.lower() not in excluded}
