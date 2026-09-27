import base64
import os
import random
import sys
import time
from pathlib import Path

# --- STATIC FFMPEG PATH INJECTION (Local E: Drive Virtual Env) ---
STATIC_FFMPEG_PATH = (
    r"E:\StemSplitterProject\.venv\Lib\site-packages\static_ffmpeg\bin\win32"
)
if os.path.exists(STATIC_FFMPEG_PATH) and STATIC_FFMPEG_PATH not in os.environ["PATH"]:
  os.environ["PATH"] = STATIC_FFMPEG_PATH + os.pathsep + os.environ["PATH"]

# --- TORCH, HUGGINGFACE & TEMP CACHE PATHS (E: Drive Only) ---
os.environ["TORCH_HOME"] = "E:/StemSplitterProject/cache/torch"
os.environ["HF_HOME"] = "E:/StemSplitterProject/cache/huggingface"
os.environ["HUGGINGFACE_HUB_CACHE"] = "E:/StemSplitterProject/cache/huggingface/hub"
os.environ["TMPDIR"] = "E:/StemSplitterProject/temp_downloads"
os.environ["TEMP"] = "E:/StemSplitterProject/temp_downloads"
os.environ["TMP"] = "E:/StemSplitterProject/temp_downloads"

import librosa
import numpy as np
import soundfile as sf
import streamlit as st
import streamlit.components.v1 as components
from pydub import AudioSegment

st.set_page_config(
    page_title="MAX Stem Splitter & Auth",
    page_icon="🎛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- SESSION STATES INITIALIZATION ---
st.session_state.splash_done = True
st.session_state.page_mode = "app_main"
st.session_state.logged_in_user = "joltaflm349@gmail.com"

if "split_done" not in st.session_state:
  st.session_state.split_done = False
if "stems_paths" not in st.session_state:
  st.session_state.stems_paths = {}
if "selected_quality" not in st.session_state:
  st.session_state.selected_quality = "Normal"
if "saved_output_format" not in st.session_state:
  st.session_state.saved_output_format = "WAV (Lossless)"

# --- STEMTUBE SESSION STATES (Default E: Drive Paths) ---
E_BASE_DOWNLOADS = r"E:\stemsplitterproject\downloads"
os.makedirs(E_BASE_DOWNLOADS, exist_ok=True)

if "output_folder" not in st.session_state:
  st.session_state.output_folder = E_BASE_DOWNLOADS
if "folder_selected" not in st.session_state:
  st.session_state.folder_selected = False
if "button_state" not in st.session_state:
  st.session_state.button_state = "CHOOSE_FOLDER"
if "download_state" not in st.session_state:
  st.session_state.download_state = "IDLE"
if "last_downloaded_file" not in st.session_state:
  st.session_state.last_downloaded_file = None
if "last_downloaded_type" not in st.session_state:
  st.session_state.last_downloaded_type = "Audio (MP3)"

# --- LOGO ENCODING ---
logo_path = r"E:\stemsplitterproject\assets\logo.png"
logo_img_tag = ""
if os.path.exists(logo_path):
  with open(logo_path, "rb") as f:
    encoded_logo = base64.b64encode(f.read()).decode()
    logo_img_tag = f'<img src="data:image/png;base64,{encoded_logo}" style="height: 26px; width: auto; margin-right: 4px; vertical-align: middle;">'

# --- MAIN APP LAYOUT & STYLING ---
st.markdown(
    """
    <style>
    /* STRICT SCROLL LOCK FOR ALL STREAMLIT CONTAINERS */
    html, body, 
    [data-testid="stAppViewContainer"], 
    [data-testid="stMain"], 
    section[data-testid="stMain"], 
    div[data-testid="stMainBlockContainer"],
    .stApp, section.main, .main {
        overflow: hidden !important;
        height: 100vh !important;
        max-height: 100vh !important;
    }

    /* SHIFT HOMEPAGE CONTENT UPWARDS (REMOVE TOP PADDING) */
    div[data-testid="stMainBlockContainer"], .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        margin-top: 0rem !important;
    }

    /* UNIFORM BOX / CARD SIZE FOR ALL FEATURE BOXES (VOICE RECORDER, ETC.) */
    div[data-testid="stHorizontalBlock"] > div > div > div[style*="border-radius"],
    div[style*="border-radius"][style*="padding"] {
        min-height: 105px !important;
        height: 105px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        box-sizing: border-box !important;
    }

    .stApp {
        background-color: #080a12 !important;
        color: #f1f5f9 !important;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }
    div[data-testid='stSidebarNav'] { display: none !important; }
    [data-testid='stSidebar'] {
        background-color: #06080e !important;
        border-right: 1px solid #161a29 !important;
        max-width: 250px !important;
        min-width: 250px !important;
        padding-top: 0px !important;
    }
    
    [data-testid='stSidebar'] > div:first-child {
        padding-top: 0px !important;
        margin-top: 0px !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
        background-color: #0d1222 !important;
        border: 1px solid #1e293b !important;
        border-radius: 6px !important;
        padding: 6px 10px !important;
        margin-bottom: 7px !important;
        box-shadow: none !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {
        background-color: #172036 !important;
        border-color: #00a8ff !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"] {
        background-color: #131b31 !important;
        border: 1px solid #00a8ff !important;
        box-shadow: 0 0 6px rgba(0, 168, 255, 0.3) !important;
    }

    [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] p {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        letter-spacing: 0.3px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
  st.markdown(
      f"""
        <div style="margin-top: -10px; margin-bottom: 12px;">
            <div style="font-size: 17px; font-weight: 900; color: #ffffff; letter-spacing: 0.5px; display: flex; align-items: center;">
                {logo_img_tag} MAX &nbsp; <span style="color: #00bfff; text-shadow: 0 0 10px rgba(0, 191, 255, 0.8);">Stem Splitter</span>
            </div>
            <div style="font-size: 12px; color: #10b981; margin-top: 2px;">👤 {st.session_state.logged_in_user}</div>
            <div style="color: #0055ff; font-size: 13px; font-weight: 900; margin-top: 14px; letter-spacing: 1px; margin-bottom: 8px;">CHOOSE CATEGORY</div>
        </div>
        """,
      unsafe_allow_html=True,
  )

  # Root directory-a awm ang vekin path kan siam tawh e:
  st.page_link("homepage.py", label="🏠 HOMEPAGE")
  st.page_link("stem_splitter.py", label="🎛️ STEM SPLITTER")
  st.page_link("voice_recorder.py", label="🎙️ VOICE RECORDER")
  st.page_link("stemtube.py", label="📥 STEMTUBE")
  st.page_link("recent_files.py", label="🕒 RECENT FILES")
  st.page_link("cloud_drive.py", label="☁️ CLOUD DRIVE")
  st.page_link("settings.py", label="⚙️ SETTINGS")

# --- HOMEPAGE CONTENT EXECUTION ---
try:
  from homepage import show_homepage

  show_homepage()
except Exception:
  st.warning("⚠️ 'homepage.py' hmuh a ni lo.")
