import os
import pathlib
import yt_dlp

# Ruta universal donde se guardarán las descargas
DOWNLOAD_DIR = pathlib.Path(__file__).parent.parent / "downloads"
DOWNLOAD_DIR.mkdir(exist_ok=True)

def get_media_info(url: str) -> dict:
    """Extrae metadatos del enlace (Título, duración, miniatura, plataforma) sin descargar."""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "thumbnail": info.get("thumbnail"),
            "uploader": info.get("uploader"),
            "platform": info.get("extractor_key")
        }

def download_media(url: str, format_type: str = "mp4") -> str:
    """
    Descarga el archivo en el formato solicitado (mp4 o mp3).
    Devuelve la ruta absoluta del archivo generado.
    """
    output_template = str(DOWNLOAD_DIR / "%(title)s.%(ext)s")
    
    if format_type == "mp3":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True
        }
    else:  # MP4
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': output_template,
            'quiet': True
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        
        if format_type == "mp3":
            filename = os.path.splitext(filename)[0] + ".mp3"
            
        return filename

if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    print("Obteniendo información de prueba...")
    info = get_media_info(test_url)
    print(f"Título: {info['title']}")
    print(f"Plataforma: {info['platform']}")