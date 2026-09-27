import base64
from datetime import datetime
import os
import time
import streamlit as st

st.set_page_config(
    page_title="MAX Recent Files",
    page_icon="🕒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Unified Theme & Styling
st.markdown(
    """
    <style>
    /* Global App Theme */
    .stApp {
        background-color: #0b0c14 !important;
        color: #ffffff !important;
        font-family: 'Segoe UI', system-ui, sans-serif;
        max-width: 100% !important;
        overflow-x: hidden !important;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    div[data-testid='stSidebarNav'] { display: none !important; }

    /* Sidebar Theme */
    [data-testid='stSidebar'] {
        background-color: #090a10 !important;
        border-right: 1px solid #1c1e2d !important;
        max-width: 240px !important;
        min-width: 240px !important;
        padding-top: 0px !important;
    }
    
    [data-testid='stSidebar'] > div:first-child {
        padding-top: 0px !important;
        margin-top: 0px !important;
    }

    [data-testid='stSidebar'] [data-testid='stVerticalBlock'] {
        gap: 10px !important;
    }

    /* Sidebar Links Box */
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
        margin-bottom: 8px !important;
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

    /* CHOOSE CATEGORY bottom margin increased to push menu items down */
    .choose-category-title {
        font-size: 13px !important;
        color: #0055ff !important;
        text-shadow: 0 0 10px #0055ff, 0 0 20px #1e90ff !important;
        font-weight: 900 !important;
        margin-bottom: 24px !important; 
        margin-top: 4px !important;
        letter-spacing: 1px !important;
    }

    /* Header Container */
    .top-header-container { 
        display: flex; 
        align-items: center; 
        margin-bottom: 16px; 
        margin-top: -10px; 
    }
    .main-logo-brand { 
        font-family: 'Arial Black', sans-serif; 
        font-size: 20px; 
        font-weight: 900; 
        color: #ffffff; 
        margin-right: 10px; 
    }
    .main-app-title { 
        font-family: 'Segoe UI', sans-serif; 
        font-size: 17px; 
        color: #06b6d4; 
        border-left: 2px solid #06b6d4; 
        padding-left: 10px; 
        font-weight: 700; 
    }

    .file-item-card {
        background-color: #101524;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
        transition: all 0.2s ease-in-out;
    }
    .file-item-card:hover {
        border-color: #06b6d4;
        box-shadow: 0 0 12px rgba(6, 182, 212, 0.2);
    }

    .file-title {
        color: #f8fafc;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 4px;
        word-break: break-all;
    }
    .file-meta {
        color: #64748b;
        font-size: 11px;
        font-weight: 600;
    }

    .empty-state {
        background-color: #0e1526;
        border: 1px dashed #1e293b;
        border-radius: 8px;
        padding: 30px;
        text-align: center;
        color: #64748b;
        font-size: 13px;
        font-weight: 600;
    }

    /* Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        border-radius: 6px !important;
        border: 1px solid #38bdf8 !important;
        font-size: 12px !important;
        min-height: 36px !important;
        color: #ffffff !important;
        font-weight: bold !important;
    }

    div[data-testid='stDownloadButton'] > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        border: 1px solid #10b981 !important;
        color: #ffffff !important;
        font-weight: bold !important;
        min-height: 36px !important;
        border-radius: 6px !important;
        font-size: 12px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar setup with Logo check from assets folder
logo_b64 = ""
possible_logo_paths = [
    "E:/stemsplitterproject/assets/logo.png",
    "E:/stemsplitterproject/assets/logo",
    "E:/StemSplitterProject/assets/logo.png",
]

for path in possible_logo_paths:
    if os.path.exists(path):
        with open(path, "rb") as lf:
            logo_b64 = base64.b64encode(lf.read()).decode()
        break

with st.sidebar:
    st.markdown(
        f"""
        <div style="margin-top: -35px;">
            <div style="display: flex; align-items: center; margin-bottom: 4px;">
                <img src="data:image/png;base64,{logo_b64}" style="width: 32px; height: 32px; margin-right: 8px; object-fit: contain;" />
                <span style="font-family: 'Segoe UI', system-ui, sans-serif; font-size: 16px; font-weight: 900; color: #ffffff; letter-spacing: 0.5px;">
                    MAX <span style="color: #00bfff; text-shadow: 0 0 10px rgba(0, 191, 255, 0.7);">Stem Splitter</span>
                </span>
            </div>
            <div class="choose-category-title">CHOOSE CATEGORY</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar links pushed down below CHOOSE CATEGORY
    st.page_link("app.py", label="🏠 HOMEPAGE")
    st.page_link("app.py", label="🎛️ STEM SPLITTER")
    st.page_link("pages/voice_recorder.py", label="🎙️ VOICE RECORDER")
    st.page_link("pages/stemtube.py", label="📥 STEMTUBE")
    st.page_link("pages/recent_files.py", label="🕒 RECENT FILES")
    st.page_link("pages/cloud_drive.py", label="☁️ CLOUD DRIVE")
    st.page_link("pages/settings.py", label="⚙️ SETTINGS")

# Main Header
st.markdown(
    '<div class="top-header-container"><span class="main-logo-brand">MAX</span><span class="main-app-title">Recent Processed Files</span></div>',
    unsafe_allow_html=True,
)

def get_file_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"

# Scan directory for recent output files
target_folder = "downloads"
os.makedirs(target_folder, exist_ok=True)

valid_extensions = [".mp3", ".wav", ".m4a", ".flac", ".mp4", ".ogg"]
files = []

for entry in os.scandir(target_folder):
    if entry.is_file() and any(
        entry.name.lower().endswith(ext) for ext in valid_extensions
    ):
        stat = entry.stat()
        files.append({
            "name": entry.name,
            "path": entry.path,
            "mtime": stat.st_mtime,
            "size": stat.st_size,
        })

# Sort by newest first
files.sort(key=lambda x: x["mtime"], reverse=True)

if not files:
    st.markdown(
        """
        <div class="empty-state">
            <div style="font-size:32px; margin-bottom:8px;">📁</div>
            <div>No recent processed files found in <code>downloads/</code> folder.</div>
            <div style="font-size:11px; margin-top:6px; color:#475569;">Exported audio files from StemSplitter or StemTube will appear here automatically.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    # RECENT FILES title (White) & SHOWING X RECENT FILES
    st.markdown(
        '<div style="font-size:22px; color:#ffffff; font-weight:900; letter-spacing:1px; margin-bottom:2px;">RECENT FILES</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div style="font-size:13px; color:#00bfff; font-weight:bold; margin-bottom:12px; letter-spacing:1px;">SHOWING {len(files)} RECENT FILES</div>',
        unsafe_allow_html=True,
    )

    for idx, f_info in enumerate(files):
        mod_time = datetime.fromtimestamp(f_info["mtime"]).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        size_str = get_file_size(f_info["size"])

        st.markdown(
            f"""
            <div class="file-item-card">
                <div class="file-title">🎵 {f_info['name']}</div>
                <div class="file-meta">Modified: {mod_time} &nbsp;|&nbsp; Size: {size_str}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c_play, c_dl, c_del = st.columns([3, 1, 1])
        with c_play:
            if f_info["name"].lower().endswith(".mp4"):
                st.video(f_info["path"])
            else:
                st.audio(f_info["path"])
        with c_dl:
            with open(f_info["path"], "rb") as f:
                st.download_button(
                    label="💾 Download",
                    data=f,
                    file_name=f_info["name"],
                    mime=(
                        "audio/mpeg"
                        if f_info["name"].endswith(".mp3")
                        else "application/octet-stream"
                    ),
                    key=f"dl_{idx}",
                    use_container_width=True,
                )
        with c_del:
            if st.button("🗑️ Delete", key=f"del_{idx}", use_container_width=True):
                try:
                    os.remove(f_info["path"])
                    st.toast(f"Deleted {f_info['name']}")
                    time.sleep(0.3)
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to delete: {e}")

        st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)