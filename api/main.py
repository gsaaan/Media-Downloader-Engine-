from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse, FileResponse
import pathlib
import os

from core.downloader import download_media

app = FastAPI(
    title="Media Engine",
    description="Motor de Descarga de Medios Multiplataforma",
    version="1.2.1"
)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Media Engine</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0b0f19;
            --card-bg: rgba(15, 23, 42, 0.65);
            --border: rgba(255, 255, 255, 0.07);
            --border-hover: rgba(255, 255, 255, 0.15);
            --accent: #38bdf8;
            --accent-glow: rgba(56, 189, 248, 0.15);
            --text-main: #f8fafc;
            --text-muted: #64748b;
            --input-bg: rgba(3, 7, 18, 0.5);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg);
            background-image: 
                radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.05) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(99, 102, 241, 0.05) 0px, transparent 50%);
            color: var(--text-main);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow-x: hidden;
            -webkit-font-smoothing: antialiased;
        }

        .container {
            width: 100%;
            max-width: 480px;
            padding: 24px;
        }

        .card {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 2.25rem;
            box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.6);
        }

        .header {
            text-align: left;
            margin-bottom: 2rem;
        }

        h1 {
            font-size: 1.5rem;
            font-weight: 700;
            letter-spacing: -0.025em;
            color: var(--text-main);
            margin-bottom: 0.4rem;
        }

        p.subtitle {
            font-size: 0.875rem;
            color: var(--text-muted);
            font-weight: 400;
            line-height: 1.4;
        }

        .input-group {
            margin-bottom: 1.25rem;
            text-align: left;
        }

        label {
            display: block;
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--text-muted);
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        input[type="text"] {
            width: 100%;
            padding: 0.85rem 1rem;
            border-radius: 10px;
            border: 1px solid var(--border);
            background: var(--input-bg);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            outline: none;
            transition: all 0.2s ease;
        }

        input[type="text"]::placeholder {
            color: #475569;
        }

        input[type="text"]:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-glow);
        }

        .options-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }

        .format-option {
            position: relative;
        }

        .format-option input {
            position: absolute;
            opacity: 0;
            width: 0;
            height: 0;
        }

        .format-label {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0.8rem;
            background: var(--input-bg);
            border: 1px solid var(--border);
            border-radius: 10px;
            cursor: pointer;
            font-weight: 500;
            font-size: 0.85rem;
            color: var(--text-muted);
            transition: all 0.2s ease;
        }

        .format-label:hover {
            border-color: var(--border-hover);
            color: var(--text-main);
        }

        .format-option input:checked + .format-label {
            border-color: var(--accent);
            background: rgba(56, 189, 248, 0.06);
            color: var(--accent);
            font-weight: 600;
        }

        button.btn-submit {
            width: 100%;
            margin-top: 1.5rem;
            padding: 0.9rem;
            border: none;
            border-radius: 10px;
            background: #f8fafc;
            color: #0f172a;
            font-weight: 600;
            font-size: 0.9rem;
            font-family: 'Inter', sans-serif;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        button.btn-submit:hover {
            background: #e2e8f0;
            transform: translateY(-1px);
        }

        button.btn-submit:active {
            transform: translateY(0);
        }

        /* Progress Status Section */
        .status-container {
            margin-top: 1.5rem;
            display: none;
            background: var(--input-bg);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1rem 1.25rem;
            text-align: left;
        }

        .status-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.6rem;
            font-size: 0.8rem;
        }

        .status-title {
            color: var(--text-main);
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .status-percentage {
            font-family: 'JetBrains Mono', monospace;
            color: var(--accent);
            font-size: 0.75rem;
        }

        .progress-bar-bg {
            width: 100%;
            height: 4px;
            background: rgba(255, 255, 255, 0.06);
            border-radius: 4px;
            overflow: hidden;
        }

        .progress-bar-fill {
            height: 100%;
            width: 0%;
            background: var(--accent);
            border-radius: 4px;
            transition: width 0.3s ease;
        }

        .status-log {
            margin-top: 0.6rem;
            font-size: 0.75rem;
            color: var(--text-muted);
        }

        .spinner {
            width: 12px;
            height: 12px;
            border: 2px solid rgba(56, 189, 248, 0.2);
            border-top-color: var(--accent);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="header">
                <h1>Media Downloader</h1>
                <p class="subtitle">Procesamiento y descarga directa de contenido multimedia.</p>
            </div>

            <form id="downloadForm">
                <div class="input-group">
                    <label for="urlInput">URL del Medio</label>
                    <input type="text" id="urlInput" name="url" placeholder="https://..." required autocomplete="off">
                </div>

                <div class="input-group">
                    <label>Formato de Salida</label>
                    <div class="options-grid">
                        <div class="format-option">
                            <input type="radio" id="fmtMp4" name="format_type" value="mp4" checked>
                            <label for="fmtMp4" class="format-label">
                                Video (MP4)
                            </label>
                        </div>
                        <div class="format-option">
                            <input type="radio" id="fmtMp3" name="format_type" value="mp3">
                            <label for="fmtMp3" class="format-label">
                                Audio (MP3)
                            </label>
                        </div>
                    </div>
                </div>

                <button type="submit" class="btn-submit" id="submitBtn">
                    Descargar
                </button>
            </form>

            <div class="status-container" id="statusBox">
                <div class="status-header">
                    <div class="status-title">
                        <div class="spinner" id="statusSpinner"></div>
                        <span id="statusState">Procesando enlace...</span>
                    </div>
                    <span class="status-percentage" id="statusPercent">0%</span>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" id="progressFill"></div>
                </div>
                <div class="status-log" id="statusLog">Iniciando petición...</div>
            </div>
        </div>
    </div>

    <script>
        const form = document.getElementById('downloadForm');
        const submitBtn = document.getElementById('submitBtn');
        const statusBox = document.getElementById('statusBox');
        const progressFill = document.getElementById('progressFill');
        const statusPercent = document.getElementById('statusPercent');
        const statusState = document.getElementById('statusState');
        const statusLog = document.getElementById('statusLog');
        const statusSpinner = document.getElementById('statusSpinner');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const url = document.getElementById('urlInput').value;
            const formatType = document.querySelector('input[name="format_type"]:checked').value;

            submitBtn.disabled = true;
            submitBtn.style.opacity = '0.5';
            statusBox.style.display = 'block';

            progressFill.style.width = '15%';
            statusPercent.innerText = '15%';
            statusState.innerText = 'Analizando metadatos...';
            statusLog.innerText = 'Extrayendo streams de información...';
            statusSpinner.style.display = 'block';

            let progress = 15;
            const interval = setInterval(() => {
                if (progress < 85) {
                    progress += Math.floor(Math.random() * 8) + 3;
                    if (progress > 85) progress = 85;
                    progressFill.style.width = progress + '%';
                    statusPercent.innerText = progress + '%';

                    if (progress > 40 && progress < 70) {
                        statusState.innerText = 'Descargando flujo...';
                        statusLog.innerText = 'Procesando paquetes de datos...';
                    } else if (progress >= 70) {
                        statusState.innerText = 'Finalizando archivo...';
                        statusLog.innerText = 'Generando contenedor ' + formatType.toUpperCase() + '...';
                    }
                }
            }, 500);

            try {
                const formData = new FormData();
                formData.append('url', url);
                formData.append('format_type', formatType);

                const response = await fetch('/download', {
                    method: 'POST',
                    body: formData
                });

                clearInterval(interval);

                if (!response.ok) {
                    const errData = await response.json();
                    throw new Error(errData.detail || 'Error en la descarga');
                }

                progressFill.style.width = '100%';
                statusPercent.innerText = '100%';
                statusState.innerText = 'Completado';
                statusLog.innerText = 'Descargando en el sistema...';
                statusSpinner.style.display = 'none';

                const blob = await response.blob();
                const contentDisposition = response.headers.get('Content-Disposition');
                let filename = 'media.' + formatType;

                if (contentDisposition) {
                    const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/);
                    if (filenameMatch && filenameMatch[1]) {
                        filename = filenameMatch[1];
                    }
                }

                const downloadUrl = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = downloadUrl;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(downloadUrl);

            } catch (err) {
                clearInterval(interval);
                progressFill.style.backgroundColor = '#ef4444';
                statusState.innerText = 'Error';
                statusPercent.innerText = 'FAIL';
                statusLog.innerText = err.message;
                statusSpinner.style.display = 'none';
            } finally {
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.style.opacity = '1';
                }, 2000);
            }
        });
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_TEMPLATE

@app.post("/download")
def handle_download(url: str = Form(...), format_type: str = Form("mp4")):
    try:
        file_path = download_media(url, format_type)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail="Error generando el archivo.")
        
        return FileResponse(
            path=file_path, 
            filename=pathlib.Path(file_path).name,
            media_type='application/octet-stream'
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar el enlace: {str(e)}")