# Media Downloader Engine

A lightweight, cross-platform media processing engine and REST API built with Python and FastAPI. The application enables seamless video and audio extraction from various streaming platforms with real-time status feedback and an optimized dark user interface.

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

cd media-downloader-engine-

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

