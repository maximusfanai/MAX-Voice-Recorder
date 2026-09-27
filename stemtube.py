import base64
import os
import re
import tempfile
import time

import streamlit as st
import yt_dlp


def sanitize_filename(name):
  name = re.sub(r"[^\x00-\x7F]+", "", name)
  name = re.sub(r'[\\/*?:"<>|#]', "", name)
  name = re.sub(r"\s+", " ", name).strip()
  return name if name else "downloaded_media"


st.set_page_config(
    page_title="StemTube Downloader",
    page_icon="📥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp { background-color: #0b0c14 !important; color: #f1f5f9 !important; font-family: 'Segoe UI', sans-serif; }
    
    .block-container {
        padding-top: 2.5rem !important;
    }

    div[data-testid='stSidebarNav'] { display: none !important; }
    
    [data-testid='stSidebar'] {
        background-color: #090a10 !important;
        border-right: 1px solid #1c1e2d !important;
        max-width: 240px !important;
        min-width: 240px !important;
        padding-top: 0px !important;
    }

    [data-testid="stSidebarHeader"] {
        position: relative !important;
        padding: 0 !important;
        height: 0 !important;
    }

    [data-testid="stSidebarCollapseButton"] {
        position: absolute !important;
        top: 295px !important;
        right: -14px !important;
        z-index: 999999 !important;
        background-color: #090a10 !important;
        border: 1.5px solid #00bfff !important;
        border-radius: 50% !important;
        color: #ffffff !important;
        width: 28px !important;
        height: 28px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 0 10px rgba(0, 191, 255, 0.5) !important;
    }

    [data-testid="stSidebarCollapseButton"] button {
        background: transparent !important;
        border: none !important;
        color: #ffffff !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
        background-color: transparent !important;
    }

    [data-testid="stSidebarCollapsedControl"] {
        display: flex !important;
        position: fixed !important;
        top: 295px !important;
        left: 0px !important;
        z-index: 999999 !important;
        background-color: #090a10 !important;
        border: 1.5px solid #00bfff !important;
        border-radius: 0 50% 50% 0 !important;
        color: #ffffff !important;
        box-shadow: 0 0 10px rgba(0, 191, 255, 0.5) !important;
    }

    [data-testid='stSidebar'] > div:first-child {
        padding-top: 0px !important;
        margin-top: 0px !important;
    }

    [data-testid='stSidebar'] [data-testid='stVerticalBlock'] {
        gap: 12px !important;
    }

    [data-testid='stSidebar'] div[data-testid='stPageLink'],
    [data-testid='stSidebar'] div[data-testid='stPageLink'] > a,
    [data-testid='stSidebar'] div[data-testid='stPageLink'][aria-current="page"],
    [data-testid='stSidebar'] div[data-testid='stPageLink'][aria-current="page"] > a,
    [data-testid='stSidebar'] div[data-testid='stPageLink']:hover,
    [data-testid='stSidebar'] div[data-testid='stPageLink']:active,
    [data-testid='stSidebar'] div[data-testid='stPageLink']:focus {
        background-color: #091326 !important;
        background-image: none !important;
        border: 1.5px solid #00bfff !important;
        border-radius: 6px !important;
        box-shadow: 0 0 14px rgba(0, 191, 255, 0.5), inset 0 0 6px rgba(0, 191, 255, 0.2) !important;
        margin-bottom: 12px !important;
        width: 100% !important;
        padding: 6px 8px !important;
        transform: none !important;
        opacity: 1 !important;
    }
    
    [data-testid='stSidebar'] div[data-testid='stPageLink'] span,
    [data-testid='stSidebar'] div[data-testid='stPageLink'] p,
    [data-testid='stSidebar'] div[data-testid='stPageLink'] div {
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 12px !important;
        background-color: transparent !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.header-title) {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: space-between !important;
        align-items: center !important;
        width: 100% !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.header-title) > div[data-testid="stColumn"] {
        width: auto !important;
        min-width: 0 !important;
        flex: 0 0 auto !important;
        display: flex !important;
        align-items: center !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.header-title) > div[data-testid="stColumn"]:last-child {
        margin-left: auto !important;
        display: flex !important;
        justify-content: flex-end !important;
        align-items: center !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.header-title) div.stButton {
        display: flex !important;
        justify-content: flex-end !important;
        align-items: center !important;
        width: auto !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.header-title) div.stButton > button {
        background: #161929 !important;
        border: 1.5px solid #00bfff !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 11px !important;
        border-radius: 5px !important;
        padding: 0px 4px !important;
        height: 22px !important;
        min-height: 22px !important;
        max-height: 22px !important;
        width: 52px !important;
        max-width: 52px !important;
        min-width: 52px !important;
        margin-top: 8px !important;
        box-shadow: 0 0 6px rgba(0, 191, 255, 0.3) !important;
        transition: all 0.2s ease !important;
        line-height: 1 !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.header-title) div.stButton > button:hover {
        background: #00bfff !important;
        color: #0b0c14 !important;
        box-shadow: 0 0 12px rgba(0, 191, 255, 0.7) !important;
    }

    .main-card {
        background: linear-gradient(145deg, #10121d 0%, #171a2b 100%);
        border: 1px solid #25283d;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    
    .header-title {
        font-size: 20px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        white-space: nowrap !important;
    }

    div[data-testid='stTextInput'] {
        width: 100% !important;
        margin-bottom: 0px !important;
    }

    div[data-testid='stTextInput'] label, 
    div[data-testid='stTextInput'] label p {
        font-size: 14px !important;
        font-weight: 800 !important;
        color: #00bfff !important;
        margin-bottom: 6px !important;
        text-transform: none !important;
        letter-spacing: 0.5px !important;
        text-shadow: 0 0 8px rgba(0, 191, 255, 0.8), 0 0 16px rgba(0, 191, 255, 0.5) !important;
    }
    
    div[data-testid='stTextInput'] input { 
        background-color: #161929 !important; 
        border: 1.5px solid #25283d !important; 
        color: #ffffff !important; 
        font-size: 14px !important; 
        height: 40px !important; 
        border-radius: 10px !important;
        padding: 0 12px !important;
        width: 100% !important;
    }

    div[data-testid='stSelectbox'] label, 
    div[data-testid='stSelectbox'] label p {
        font-size: 14px !important;
        font-weight: 800 !important;
        color: #00bfff !important;
        margin-bottom: 6px !important;
        text-transform: none !important;
        letter-spacing: 0.5px !important;
        text-shadow: 0 0 8px rgba(0, 191, 255, 0.8), 0 0 16px rgba(0, 191, 255, 0.5) !important;
    }

    .open-stemtube-btn {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
        background: linear-gradient(135deg, #06b6d4 0%, #0284c7 100%) !important;
        color: #ffffff !important;
        padding: 10px 18px !important;
        border-radius: 10px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        text-decoration: none !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 14px rgba(6, 182, 212, 0.4) !important;
        width: auto !important;
    }

    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(135deg, #06b6d4 0%, #0284c7 100%) !important; 
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        border: none !important;
        height: 35px !important;
        min-height: 35px !important;
        width: 130px !important;
        margin-left: 0px !important;
        margin-top: 8px !important;
        padding: 0 12px !important;
        box-shadow: 0 4px 14px rgba(6, 182, 212, 0.4) !important;
        transition: all 0.3s ease;
    }

    div[data-testid="stVideo"] {
        max-width: 100% !important;
        width: 100% !important;
        margin: 0 auto !important;
    }
    div[data-testid="stVideo"] video {
        width: 100% !important;
        max-width: 480px !important;
        height: auto !important;
        max-height: 280px !important;
        display: block !important;
        margin: 0 auto !important;
        border-radius: 12px !important;
        border: 1px solid #25283d !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.window-control-wrapper) {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: flex-end !important;
        align-items: center !important;
        gap: 4px !important;
        width: 100% !important;
    }

    div[data-testid="stColumn"]:has(.window-control-wrapper) {
        width: auto !important;
        min-width: 0 !important;
        flex: 0 0 auto !important;
    }

    div[data-testid="stColumn"]:has(.window-control-wrapper) button {
        background: transparent !important;
        background-color: transparent !important;
        background-image: none !important;
        border: none !important;
        box-shadow: none !important;
        color: #ffffff !important;
        font-size: 14px !important;
        font-weight: bold !important;
        width: 24px !important;
        height: 24px !important;
        min-height: 24px !important;
        max-height: 24px !important;
        min-width: 24px !important;
        border-radius: 50% !important;
        padding: 0 !important;
        margin: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: background-color 0.2s ease !important;
    }

    div[data-testid="stColumn"]:has(.window-control-wrapper) button:hover {
        background-color: rgba(255, 255, 255, 0.2) !important;
        color: #ffffff !important;
    }
    
    div[data-testid='InputInstructions'] { display: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

if "download_state" not in st.session_state:
  st.session_state.download_state = "IDLE"
if "last_downloaded_file" not in st.session_state:
  st.session_state.last_downloaded_file = None
if "selected_format" not in st.session_state:
  st.session_state.selected_format = "Audio (MP3)"
if "selected_quality" not in st.session_state:
  st.session_state.selected_quality = "320kbps"
if "media_visible" not in st.session_state:
  st.session_state.media_visible = True
if "media_minimized" not in st.session_state:
  st.session_state.media_minimized = False

yt_svg = """<svg width="18" height="13" viewBox="0 0 28 20" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; margin-right: 6px; filter: drop-shadow(0 0 6px #0038ff);"><rect width="28" height="20" rx="5" fill="#0038ff"/><path d="M11 5.5L19 10L11 14.5V5.5Z" fill="white"/></svg>"""

logo_path = r"E:\stemsplitterproject\assets\logo.png"
logo_img_tag = ""

if os.path.exists(logo_path):
  try:
    with open(logo_path, "rb") as f:
      encoded_logo = base64.b64encode(f.read()).decode("utf-8")
      logo_img_tag = f'<img src="data:image/png;base64,{encoded_logo}" style="height: 24px; width: auto; margin-right: 8px; vertical-align: middle;" />'
  except Exception as e:
    print(f"Error loading logo: {e}")

with st.sidebar:
  if logo_img_tag:
    st.markdown(
        f"""
            <div style="display: flex; align-items: center; margin-bottom: 4px; padding-top: 10px;">
                {logo_img_tag}
                <span style="font-size: 14px; font-weight: 900; color: #ffffff; letter-spacing: 0.5px;">MAX Stem Splitter</span>
            </div>
            <div style="color: #ffffff; font-size: 13px; font-weight: 900; margin-top: 15px; margin-bottom: 12px; letter-spacing: 1px;">CHOOSE CATEGORY</div>
            """,
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        """
            <div style="font-size: 14px; font-weight: 900; color: #ffffff; margin-bottom: 4px; padding-top: 10px;">MAX Stem Splitter</div>
            <div style="color: #ffffff; font-size: 13px; font-weight: 900; margin-top: 15px; margin-bottom: 12px; letter-spacing: 1px;">CHOOSE CATEGORY</div>
            """,
        unsafe_allow_html=True,
    )

  st.page_link("app.py", label="🏠 HOMEPAGE")
  st.page_link("pages/stem_splitter.py", label="🎛️ STEM SPLITTER")
  st.page_link("pages/voice_recorder.py", label="🎙️ VOICE RECORDER")
  st.page_link("pages/stemtube.py", label="📥 STEMTUBE")
  st.page_link("pages/recent_files.py", label="🕒 RECENT FILES")
  st.page_link("pages/cloud_drive.py", label="☁️ CLOUD DRIVE")
  st.page_link("pages/settings.py", label="⚙️ SETTINGS")

col_title, col_back = st.columns([88, 12], vertical_alignment="center")

with col_title:
  header_logo_html = logo_img_tag if logo_img_tag else "📥 "
  st.markdown(
      f'<div class="header-title">{header_logo_html}StemTube Downloader</div>',
      unsafe_allow_html=True,
  )

with col_back:
  if st.button("Back", key="top_back_button"):
    st.switch_page("app.py")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    f'<a href="https://www.youtube.com" target="_blank" class="open-stemtube-btn">{yt_svg}<span>Open StemTube</span></a>',
    unsafe_allow_html=True,
)

youtube_url = st.text_input(
    "Youtube Link", placeholder="Paste YouTube link here..."
)

col_fmt, col_qual = st.columns(2)

with col_fmt:
  selected_format_input = st.selectbox(
      "Format",
      ["Audio (MP3)", "Video (MP4)"],
      index=0 if st.session_state.selected_format == "Audio (MP3)" else 1,
      key="fmt_box",
  )
  if selected_format_input != st.session_state.selected_format:
    st.session_state.selected_format = selected_format_input
    if "Audio" in selected_format_input:
      st.session_state.selected_quality = "320kbps"
    else:
      st.session_state.selected_quality = "1080p"
    st.rerun()

with col_qual:
  is_video = "Video" in st.session_state.selected_format
  qual_options = (
      ["1080p", "720p", "360p", "240p", "144p"]
      if is_video
      else ["320kbps", "192kbps", "128kbps"]
  )

  if st.session_state.selected_quality not in qual_options:
    st.session_state.selected_quality = qual_options[0]

  selected_quality_input = st.selectbox(
      "Quality",
      qual_options,
      index=qual_options.index(st.session_state.selected_quality),
      key="qual_box",
  )
  if selected_quality_input != st.session_state.selected_quality:
    st.session_state.selected_quality = selected_quality_input
    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

progress_bar = st.empty()

if st.session_state.download_state == "DOWNLOADING":
  btn_label = "⏳ Downloading..."
elif st.session_state.download_state == "COMPLETE":
  btn_label = "✅ Complete!"
else:
  btn_label = "🚀 Download"

download_clicked = st.button(btn_label, type="primary")

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------------
# DOWNLOADED MEDIA PLAYER & SAVE BUTTON
# -------------------------------------------------------------
if (
    st.session_state.download_state == "COMPLETE"
    and st.session_state.last_downloaded_file
    and os.path.exists(st.session_state.last_downloaded_file)
):
  with open(st.session_state.last_downloaded_file, "rb") as f:
    file_bytes = f.read()

  orig_file_name = os.path.basename(st.session_state.last_downloaded_file)
  is_audio = "Audio" in st.session_state.last_downloaded_type

  if st.session_state.media_visible:
    col_dummy, col_min_btn, col_close_btn = st.columns([0.86, 0.07, 0.07])

    with col_min_btn:
      st.markdown(
          '<div class="window-control-wrapper"></div>',
          unsafe_allow_html=True,
      )
      min_symbol = "🗖" if st.session_state.media_minimized else "−"
      if st.button(min_symbol, key="min_media_btn"):
        st.session_state.media_minimized = not st.session_state.media_minimized
        st.rerun()

    with col_close_btn:
      st.markdown(
          '<div class="window-control-wrapper"></div>',
          unsafe_allow_html=True,
      )
      if st.button("✕", key="close_media_btn"):
        st.session_state.media_visible = False
        st.rerun()

    if is_audio or st.session_state.media_minimized:
      st.audio(file_bytes)
    else:
      st.video(file_bytes)
  else:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("👁️ Show Player", key="show_media_btn"):
      st.session_state.media_visible = True
      st.rerun()

  st.markdown("<br>", unsafe_allow_html=True)

  st.download_button(
      label=f"📥 Save File:   {orig_file_name}",
      data=file_bytes,
      file_name=orig_file_name,
      mime="audio/mp3" if is_audio else "video/mp4",
      use_container_width=True,
  )

  st.markdown("<br>", unsafe_allow_html=True)

last_pct = [-1]


def progress_hook(d):
  if d["status"] == "downloading":
    try:
      dl = d.get("downloaded_bytes", 0)
      tot = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
      if tot > 0:
        pct = min(int(dl * 100 / tot), 100)
        if pct - last_pct[0] >= 2 or pct == 100:
          last_pct[0] = pct
          progress_bar.progress(pct, text=f"Downloading... {pct}%")
      else:
        simulated = (int(time.time() * 5) % 80) + 10
        progress_bar.progress(
            simulated, text="Downloading... (Fetching stream)"
        )
    except Exception:
      pass
  elif d["status"] == "finished":
    progress_bar.progress(100, text="Processing / Converting media...")


if download_clicked and st.session_state.download_state == "IDLE":
  active_url = youtube_url.strip() if youtube_url else ""
  if not active_url:
    st.warning("Khawngaihin YouTube link dah hmasa rawh.")
  else:
    # 15 SECONDS AD TIMER
    ad_box = st.empty()
    for sec in range(15, 0, -1):
      ad_box.markdown(
          f"""
            <div style="background: #161929; border: 1.5px solid #00bfff; padding: 20px; border-radius: 12px; text-align: center; margin: 15px 0; box-shadow: 0 0 20px rgba(0, 191, 255, 0.4);">
                <p style="color: #00bfff; font-weight: 800; margin: 0; font-size: 14px; text-shadow: 0 0 8px rgba(0, 191, 255, 0.8);">📺 Sponsored Ad (StemTube Processing)...</p>
                <h2 style="color: #ffcc00; font-weight: 900; margin: 8px 0 0 0; font-size: 36px; text-shadow: 0 0 10px rgba(255, 204, 0, 0.5);">{sec}s</h2>
            </div>
            """,
          unsafe_allow_html=True,
      )
      time.sleep(1)
    ad_box.empty()

    st.session_state.download_state = "DOWNLOADING"
    st.session_state.media_visible = True

    progress_bar.progress(5, text="⏳ Starting download...")

    try:
      temp_dir = tempfile.gettempdir()
      active_format = st.session_state.selected_format
      active_quality = st.session_state.selected_quality

      if "Audio" in active_format:
        ydl_opts = {
            "format": "bestaudio/best",
            "noplaylist": True,
            "restrictfilenames": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": {
                        "128kbps": "128",
                        "192kbps": "192",
                    }.get(active_quality, "320"),
                }
            ],
            "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
            "progress_hooks": [progress_hook],
        }
      else:
        h = {"144p": "144", "240p": "240", "360p": "360", "720p": "720"}.get(
            active_quality, "1080"
        )
        ydl_opts = {
            "format": (
                f"bestvideo[height<={h}]+bestaudio/best[height<={h}]/best"
            ),
            "noplaylist": True,
            "restrictfilenames": True,
            "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
            "progress_hooks": [progress_hook],
        }

      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(active_url, download=True)

        dl_file = None
        if "requested_downloads" in info and info["requested_downloads"]:
          dl_file = info["requested_downloads"][0].get("filepath")

        if not dl_file or not os.path.exists(dl_file):
          filename = ydl.prepare_filename(info)
          base, _ = os.path.splitext(filename)
          target_file = base + (
              "." + ("mp3" if "Audio" in active_format else "mp4")
          )
          if os.path.exists(target_file):
            dl_file = target_file
          elif os.path.exists(filename):
            dl_file = filename

        if dl_file and os.path.exists(dl_file):
          st.session_state.last_downloaded_file = os.path.abspath(dl_file)

        st.session_state.last_downloaded_type = active_format

      progress_bar.progress(100, text="✨ Complete!")
      time.sleep(0.4)

      st.session_state.download_state = "COMPLETE"
      st.rerun()

    except Exception as e:
      progress_bar.empty()
      st.error(f"Error: {e}")
      st.session_state.download_state = "IDLE"
      st.rerun()