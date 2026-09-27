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
    page_title="MAX Stem Splitter",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed",
)


def show_homepage():
  logo_path = os.path.join("assets", "logo.png")
  logo_img_html = ""
  if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
      encoded_logo = base64.b64encode(f.read()).decode()
      logo_img_html = f'<img src="data:image/png;base64,{encoded_logo}" style="height: 26px; width: auto; margin-right: 8px; display: inline-block;">'

  st.markdown(
      """
    <style>
        /* Slide/Scroll lo tur leh screen pumin lock tura siam */
        html, body {
            overflow: hidden !important;
            height: 100vh !important;
        }
        .stApp {
            background-color: #050811;
            color: #FFFFFF;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            overflow: hidden !important;
            height: 100vh !important;
        }
        .main .block-container {
            padding-top: 0.8rem;
            padding-bottom: 2rem;
            max-width: 560px;
            margin: 0 auto;
            overflow: hidden !important;
            max-height: 100vh !important;
        }

        div[data-testid='stSidebar'] {
            display: none !important;
        }
        header[data-testid="stHeader"] {
            display: none !important;
        }

        /* Card Link Override */
        a.card-link {
            text-decoration: none !important;
            color: inherit !important;
            display: block;
        }

        /* Top Bar Header */
        .top-bar-container {
            display: flex !important;
            justify-content: space-between !important;
            align-items: center !important;
            padding: 2px 0px 14px 0px !important;
            width: 100% !important;
        }
        .logo-title {
            font-size: 21px !important;
            font-weight: 800;
            margin: 0;
            line-height: 1;
            color: #FFFFFF;
            display: flex !important;
            align-items: center !important;
        }
        .logo-title span {
            background: linear-gradient(90deg, #A855F7, #EC4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .logo-sub {
            font-size: 10px;
            color: #9CA3AF;
            letter-spacing: 1px;
            font-weight: 700;
            margin-top: 4px;
        }
        .top-actions {
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
        }
        .pro-badge {
            background: rgba(234, 179, 8, 0.2);
            color: #EAB308;
            border: 1px solid rgba(234, 179, 8, 0.6);
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 800;
            white-space: nowrap;
        }
        .profile-btn {
            background: rgba(255, 255, 255, 0.12);
            border: 1px solid rgba(255, 255, 255, 0.25);
            width: 34px;
            height: 34px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
        }

        /* Big Cards Grid */
        .grid-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 12px;
        }
        /* Make the last big card span across both columns for a balanced layout */
        .grid-container > a:nth-child(3) {
            grid-column: span 2;
        }

        .big-card {
            border-radius: 14px;
            padding: 14px 16px;
            position: relative;
            min-height: 125px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            cursor: pointer;
        }
        .card-splitter {
            background: linear-gradient(145deg, rgba(45, 15, 70, 0.98), rgba(20, 8, 35, 1));
            border: 1px solid rgba(168, 85, 247, 0.5);
        }
        .card-recorder {
            background: linear-gradient(145deg, rgba(10, 45, 50, 0.98), rgba(5, 22, 25, 1));
            border: 1px solid rgba(20, 184, 166, 0.5);
        }
        .card-stemtube {
            background: linear-gradient(145deg, rgba(60, 15, 25, 0.98), rgba(25, 6, 12, 1));
            border: 1px solid rgba(239, 68, 68, 0.5);
        }
        .card-icon {
            font-size: 24px;
            margin-bottom: 5px;
        }
        .card-title {
            font-size: 16px;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 3px;
        }
        .card-text {
            font-size: 11.5px;
            color: #D1D5DB;
            line-height: 1.3;
        }
        .arrow-btn {
            position: absolute;
            bottom: 12px;
            right: 12px;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            color: #FFFFFF;
        }
        .arrow-purple { background: rgba(147, 51, 234, 0.5); border: 1px solid rgba(168, 85, 247, 0.8); }
        .arrow-green { background: rgba(13, 148, 136, 0.5); border: 1px solid rgba(20, 184, 166, 0.8); }
        .arrow-red { background: rgba(220, 38, 38, 0.5); border: 1px solid rgba(239, 68, 68, 0.8); }

        /* Tools Cards */
        .tools-grid {
            display: grid;
            gap: 10px;
            margin-bottom: 10px;
        }
        .tool-card {
            background: linear-gradient(135deg, rgba(20, 45, 90, 0.95), rgba(10, 25, 55, 0.98));
            border: 1px solid rgba(59, 130, 246, 0.5);
            border-radius: 12px;
            padding: 12px 14px;
            min-height: 85px;
            position: relative;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .tool-icon {
            font-size: 18px;
            margin-bottom: 4px;
        }
        .tool-title {
            font-size: 13.5px;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 2px;
        }
        .tool-sub {
            font-size: 10.5px;
            color: #BFDBFE;
            line-height: 1.2;
        }
        .tool-arrow {
            position: absolute;
            bottom: 8px;
            right: 8px;
            font-size: 12px;
            color: #93C5FD;
        }
    </style>
    """,
      unsafe_allow_html=True,
  )

  # Top Bar Header
  st.markdown(
      f"""
        <div class="top-bar-container">
            <div>
                <div class="logo-title">{logo_img_html}MAX &nbsp;<span>Stem Splitter</span></div>
                <div class="logo-sub">STEM SPLITTER & AUDIO STUDIO</div>
            </div>
            <div class="top-actions">
                <div class="pro-badge">👑 PRO</div>
                <div class="profile-btn">👤</div>
            </div>
        </div>
    """,
      unsafe_allow_html=True,
  )

  # Main Grid (3 Big Feature Cards)
  st.markdown(
      """
        <div class="grid-container">
            <a href="/stem_splitter" target="_self" class="card-link">
                <div class="big-card card-splitter">
                    <div>
                        <div class="card-icon" style="color: #C084FC;">📊</div>
                        <div class="card-title">Stem Splitter</div>
                        <div class="card-text">Split vocals, drums, bass, guitar and more.</div>
                    </div>
                    <div class="arrow-btn arrow-purple">&rarr;</div>
                </div>
            </a>
            <a href="/voice_recorder" target="_self" class="card-link">
                <div class="big-card card-recorder">
                    <div>
                        <div class="card-icon" style="color: #2DD4BF;">🎙️</div>
                        <div class="card-title">Voice Recorder</div>
                        <div class="card-text">Record, edit and save your voice or instruments.</div>
                    </div>
                    <div class="arrow-btn arrow-green">&rarr;</div>
                </div>
            </a>
            <a href="/stemtube" target="_self" class="card-link">
                <div class="big-card card-stemtube">
                    <div>
                        <div class="card-icon" style="color: #F87171;">▶️</div>
                        <div class="card-title">StemTube</div>
                        <div class="card-text">Find and download stems from YouTube.</div>
                    </div>
                    <div class="arrow-btn arrow-red">&rarr;</div>
                </div>
            </a>
        </div>
    """,
      unsafe_allow_html=True,
  )

  # Tools Row 1 (Recent Files and Cloud Drive)
  st.markdown(
      """
        <div class="tools-grid" style="grid-template-columns: 1fr 1fr;">
            <a href="/recent_files" target="_self" class="card-link">
                <div class="tool-card">
                    <div class="tool-icon" style="color: #C084FC;">🕒</div>
                    <div class="tool-title">Recent Files</div>
                    <div class="tool-sub">Quick access to files.</div>
                    <div class="tool-arrow">&rsaquo;</div>
                </div>
            </a>
            <a href="/cloud_drive" target="_self" class="card-link">
                <div class="tool-card">
                    <div class="tool-icon" style="color: #38BDF8;">☁️</div>
                    <div class="tool-title">Cloud Drive</div>
                    <div class="tool-sub">Access files anywhere.</div>
                    <div class="tool-arrow">&rsaquo;</div>
                </div>
            </a>
        </div>
    """,
      unsafe_allow_html=True,
  )

  # Tools Row 2 (Setting card only, spanning full width)
  st.markdown(
      """
        <div class="tools-grid" style="grid-template-columns: 1fr;">
            <a href="/settings" target="_self" class="card-link">
                <div class="tool-card">
                    <div class="tool-icon" style="color: #9CA3AF;">⚙️</div>
                    <div class="tool-title">Setting</div>
                    <div class="tool-sub">Customize your experience.</div>
                    <div class="tool-arrow">&rsaquo;</div>
                </div>
            </a>
        </div>
    """,
      unsafe_allow_html=True,
  )


if __name__ == "__main__":
  show_homepage()