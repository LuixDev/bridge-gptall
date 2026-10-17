api = http://localhost:8000/v1/chat/completions

para correr llms
python -m uvicorn main:app --host 127.0.0.1 --port 8000

ejercicio de ejemplo llms local
python chat.py

cd "e:\Desktop\ruta\gpt4all-bridge"
py -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m uvicorn main:app --host 0.0.0.0 --port 8000
