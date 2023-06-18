import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request, Body
from fastapi.responses import FileResponse, StreamingResponse
import os
from supabase import create_client, Client
import time

app = FastAPI()
# URL e Chave de acesso SupaBase
url: str = "https://ibkuxlzvmlulkfhmleje.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlia3V4bHp2bWx1bGtmaG1sZWplIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY4Njc3MTU0OSwiZXhwIjoyMDAyMzQ3NTQ5fQ.--yu4rL0aWhwG6jOvofDGBVXe_vvEuTb_aLV2T6u5TA"
supabase: Client = create_client(url, key)

# Nome do bucket utilizado
bucket_name: str = "imgs"

@app.get("/list")
async def list():
    # Lista todas as imagens do Bucket
    res = supabase.storage.from_(bucket_name).list()
    return res
    print(res)

@app.post("/upload")
def upload(content: UploadFile = fastapi.File(...)):
    filename = f'pic{time.time()}.png'
    with open(f"recebidos/{filename}", 'wb') as f:
        dados = content.file.read()
        f.write(dados)
    with open(os.path.join("recebidos", filename), 'rb+') as f:
        dados = f.read()
        res = supabase.storage.from_(bucket_name).upload(f"{time.time()}_{filename}", dados)
        print(res)
    return {"status": "ok"}

@app.post("/images")
def images():
    list_files = os.listdir("recebidos")
    # Rota da imagem local para ser feito o upload
    for arquivo in list_files:
        with open(os.path.join("./recebidos/", arquivo), 'rb+') as f:
            dados = f.read()
            print('cheguei aqui')
            res = supabase.storage.from_(bucket_name).upload(f"{time.time()}_{arquivo}", dados)
    return {"message": "Imagem carregada com sucesso"}
