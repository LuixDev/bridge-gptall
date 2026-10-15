from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
import requests
import json
import time

app = FastAPI()

GPT4ALL_URL = "http://localhost:4891/v1/chat/completions"


@app.post("/v1/chat/completions")
async def chat(request: Request):

    data = await request.json()

    print("\n===== PETICION DE CONTINUE =====")
    print(json.dumps(data, indent=2))

    # Guardamos si Continue quiere streaming
    use_stream = data.get("stream", False)

    # Eliminar cosas que GPT4All no soporta
    data.pop("stream_options", None)
    data.pop("tools", None)
    data.pop("tool_choice", None)
    data.pop("response_format", None)

    # GPT4All trabaja sin stream
    data["stream"] = False


    print("\n===== ENVIANDO A GPT4ALL =====")
    print(json.dumps(data, indent=2))


    response = requests.post(
        GPT4ALL_URL,
        json=data,
        timeout=600
    )


    print("\n===== RESPUESTA GPT4ALL =====")
    print(response.text)


    if response.status_code != 200:
        return JSONResponse(
            status_code=response.status_code,
            content={
                "error": response.text
            }
        )


    result = response.json()


    # Si Continue pidió stream, simulamos streaming
    if use_stream:
        return StreamingResponse(
            fake_stream(result),
            media_type="text/event-stream"
        )


    return result



def fake_stream(result):

    text = result["choices"][0]["message"]["content"]


    chunk = {
        "id": "chatcmpl-local",
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": "Llama-3-8B-Instruct",
        "choices": [
            {
                "index": 0,
                "delta": {
                    "content": text
                },
                "finish_reason": None
            }
        ]
    }


    yield "data: " + json.dumps(chunk) + "\n\n"

    yield "data: [DONE]\n\n"



@app.get("/v1/models")
def models():

    return {
        "object": "list",
        "data": [
            {
                "id": "Llama-3-8B-Instruct",
                "object": "model"
            }
        ]
    }