from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from models.url_models import URLItem, URLList
from services.youtube_service import efetuar_download, efetuar_download_de_varios

app = FastAPI(title="API para baixar musica de videos do youtube")

@app.post("/baixar", )
async def baixar(item: URLItem):
  buffer, filename = efetuar_download(item.url)
  if buffer:
    return StreamingResponse(buffer, media_type="audio/mpeg", headers={"Content-Disposition": f"attachment; filename={filename}"})
  return {"error": "Erro ao baixar a música"}

@app.post("/baixarVarios")
async def baixar_varios(item: URLList):
  zip_buffer, nome_zip = efetuar_download_de_varios(item.urls)
  return StreamingResponse(zip_buffer, media_type="application/zip", headers={"Content-Disposition": f"attachment; filename={nome_zip}"})
  
