# Media Downloader Engine

A lightweight, cross-platform media processing engine and REST API built with Python and FastAPI. The application enables seamless video and audio extraction from various streaming platforms with real-time status feedback and an optimized dark user interface.

## System Architecture

The project is structured with a clean separation of concerns, decoupling the core processing module from the presentation layer:

MediaDownloader/
ÃÄÄ core/
³   ÀÄÄ downloader.py   # Core extraction engine wrapping yt-dlp & FFmpeg
ÃÄÄ api/
³   ÀÄÄ main.py         # FastAPI application & lightweight Web Interface
ÃÄÄ downloads/          # Local storage for converted media
ÃÄÄ run.py              # Application entry point
ÃÄÄ requirements.txt    # Project dependencies
ÀÄÄ .gitignore          # Git exclusion rules

## Features

- Cross-platform support (Windows, macOS, Linux).
- Asynchronous API endpoints using FastAPI and Uvicorn.
- Dual-format media conversion: High-quality MP4 (video) and 192kbps MP3 (audio).
- Automated dependency resolution and file cleanup pipeline.
- Modern glassmorphism UI built with vanilla CSS, Inter typography, and asynchronous JavaScript fetching.

## Prerequisites

Ensure Python 3.10+ and FFmpeg are installed on your system before proceeding.

### Installing FFmpeg

#### Windows (PowerShell)
winget install Gyan.FFmpeg

#### macOS (Homebrew)
brew install ffmpeg

#### Linux (Debian/Ubuntu)
sudo apt update && sudo apt install ffmpeg -y

## Installation Steps

### 1. Clone the Repository
git clone https://github.com/gsaaan/Media-Downloader-Engine-.git
cd media-downloader-engine

### 2. Set Up Virtual Environment

#### Windows
py -m venv venv

#### macOS / Linux
python3 -m venv venv

### 3. Install Dependencies

#### Windows
.\venv\Scripts\python.exe -m pip install -r requirements.txt

#### macOS / Linux
./venv/bin/pip install -r requirements.txt

## Running the Application

### Windows
.\venv\Scripts\python.exe run.py

### macOS / Linux
./venv/bin/python run.py

Access the application by opening http://127.0.0.1:8000 in your web browser.

