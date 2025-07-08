import yt_dlp
import tempfile
import os
from io import BytesIO
from zipfile import ZipFile

def efetuar_download(url_video: str):
  with tempfile.TemporaryDirectory() as temp_dir:
    path_template = os.path.join(temp_dir, "%(title)s.%(ext)s")
        
    ydl_opts = {
      'format': 'bestaudio/best',
      'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
      }],
      'outtmpl': path_template,
      'quiet': True,
      'noplaylist': True,
      'ignoreerrors': True, 
      'geo_bypass': True, 
      'nocheckcertificate': True,      
      'no_warnings': True, 
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      info = ydl.extract_info(url_video, download=True)
      title = info.get("title", "musica")
      filename = f"{title}.mp3"
      filepath = os.path.join(temp_dir, filename)

      with open(filepath, "rb") as f:
        audio_bytes = BytesIO(f.read())
        audio_bytes.seek(0)
        return audio_bytes, filename
      
def efetuar_download_de_varios(urls: list[str]):
  with tempfile.TemporaryDirectory() as temp_dir:
    arquivos_mp3 = []

    ydl_opts = {
      'format': 'bestaudio/best',
      'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
      }],
      'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
      'quiet': True,
      'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      for url in urls:
        try:
          info = ydl.extract_info(url, download=True)
          title = info.get("title", "musica")
          nome_arquivo = f"{title}.mp3"
          caminho_arquivo = os.path.join(temp_dir, nome_arquivo)

          if os.path.exists(caminho_arquivo):
            arquivos_mp3.append(caminho_arquivo)
        except Exception as e:
          print(f"Erro ao baixar {url}: {e}")
        
    zip_buffer = BytesIO()
    with ZipFile(zip_buffer, "w") as zip_file:
      for arquivo in arquivos_mp3:
        zip_file.write(arquivo, arcname=os.path.basename(arquivo))
        
    zip_buffer.seek(0)
    return zip_buffer, "musicas.zip"