import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request, Body
from fastapi.responses import FileResponse, StreamingResponse
import os
from supabase import create_client, Client
import asyncio
import aiofiles
import time

app = FastAPI()
# URL e Chave de acesso
url: str = "https://ibkuxlzvmlulkfhmleje.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlia3V4bHp2bWx1bGtmaG1sZWplIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY4Njc3MTU0OSwiZXhwIjoyMDAyMzQ3NTQ5fQ.--yu4rL0aWhwG6jOvofDGBVXe_vvEuTb_aLV2T6u5TA"
supabase: Client = create_client(url, key)

#Nome do bucket utilizado
bucket_name: str = "ponderada"
@app.get("/list")
async def list():
    # Lista todas as imagens do Bucket
    res = supabase.storage.from_(bucket_name).list()
    print(res)

@app.post("/upload")
def upload(content: UploadFile = fastapi.File(...)):
    with open(f"recebidos/fire{time.time()}.png", 'wb') as f:
        dados = content.file.read()
        f.write(dados)
        #pass
    return {"status": "ok"}

list_files = os.listdir("recebidos")

@app.post("/images")
def images():
    # Rota da imagem local para ser feito o upload (no meu caso esta na pasta mock e é a imagem "lala.png")
    for arquivo in list_files:
        with open(os.path.join("recebidos", arquivo), 'rb+') as f:
            dados = f.read()
            res = supabase.storage.from_(bucket_name).upload(f"{time.time()}_{arquivo}", dados)
    return {"message": "Image uploaded successfully"}