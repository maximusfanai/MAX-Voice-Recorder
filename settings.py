import atexit
import base64
import json
import os
import shutil
import streamlit as st

CONFIG_FILE = "config.json"

DEFAULT_SETTINGS = {
    "app_theme": "Dark Mode (Default)",
    "export_format": "MP3",
    "export_bitrate": "320 kbps",
    "processing_engine": "CPU (Default)",
    "output_folder": "downloads",
    "auto_cleanup": True,
}


def load_config():
    config = DEFAULT_SETTINGS.copy()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config.update(json.load(f))
        except Exception:
            pass
    return config


def save_config(data):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Config save error: {e}")
        return False


def clean_temporary_files():
    cfg = load_config()
    if cfg.get("auto_cleanup", True):
        out_dir = cfg.get("output_folder", "downloads")
        target_dirs = ["temp", os.path.join(out_dir, "temp"), "cache_temp"]
        cleaned_count = 0
        for target in target_dirs:
            if os.path.exists(target) and os.path.isdir(target):
                for item in os.listdir(target):
                    item_path = os.path.join(target, item)
                    try:
                        if os.path.isfile(item_path) or os.path.islink(item_path):
                            os.unlink(item_path)
                            cleaned_count += 1
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                            cleaned_count += 1
                    except Exception:
                        pass
        return cleaned_count
    return 0


atexit.register(clean_temporary_files)

st.set_page_config(
    page_title="MAX Settings",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

saved_cfg = load_config()
for key, default_val in DEFAULT_SETTINGS.items():
    if key not in st.session_state:
        st.session_state[key] = saved_cfg.get(key, default_val)

logo_b64 = ""
logo_paths = [
    r"E:/maxstemsplitter project/logo.png",
    r"E:/StemSplitterProject/cache/logo.png",
    r"E:\stemsplitterproject\assets\logo.png",
    "logo.png",
]
for path in logo_paths:
    if os.path.exists(path):
        try:
            with open(path, "rb") as lf:
                logo_b64 = base64.b64encode(lf.read()).decode()
            break
        except Exception:
            pass

logo_img_tag = (
    f'<img src="data:image/png;base64,{logo_b64}" style="height: 24px; width: auto; margin-right: 8px; vertical-align: middle;" />'
    if logo_b64
    else ""
)


def get_theme_css(theme):
    if theme == "Glassmorphic Dark":
        bg_color = (
            "radial-gradient(circle at 50% 30%, #1e2640 0%, #0c0e18 100%)"
            " !important"
        )
        card_bg = "rgba(255, 255, 255, 0.05)"
        card_border = "1px solid rgba(255, 255, 255, 0.15)"
        accent_color = "#38bdf8"
    elif theme == "Cyberpunk Blue Neon":
        bg_color = "#030712 !important"
        card_bg = "linear-gradient(145deg, #050b18 0%, #0a1738 100%)"
        card_border = "1px solid #00f0ff"
        accent_color = "#00f0ff"
    else:
        bg_color = "#0b0c14 !important"
        card_bg = "linear-gradient(145deg, #0e121e 0%, #161b2e 100%)"
        card_border = "1px solid #232a42"
        accent_color = "#06b6d4"

    return f"""
    <style>
    header[data-testid="stHeader"] {{ background: transparent !important; }}
    .stApp {{ background: {bg_color}; color: #ffffff !important; font-family: 'Segoe UI', system-ui, sans-serif; }}
    .block-container {{
        padding-top: 1rem !important; padding-bottom: 2rem !important; max-width: 720px !important;
        background: {card_bg} !important; border: {card_border} !important; border-radius: 12px !important;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.5) !important;
    }}
    div[data-testid='stSidebarNav'] {{ display: none !important; }}
    
    [data-testid='stSidebar'] {{
        background-color: #090a10 !important;
        border-right: 1px solid #1c1e2d !important;
        max-width: 240px !important;
        min-width: 240px !important;
        padding-top: 0px !important;
    }}

    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"],
    div[data-testid="stSidebarHeader"] {{
        display: flex !important;
        visibility: visible !important;
        margin-top: 35px !important;
        padding-top: 10px !important;
        transform: translateY(15px) !important;
        z-index: 999999 !important;
    }}
    
    [data-testid='stSidebar'] > div:first-child {{
        padding-top: 0px !important;
        margin-top: -65px !important;
    }}

    [data-testid='stSidebar'] [data-testid='stVerticalBlock'] {{
        gap: 6px !important;
    }}

    [data-testid='stSidebar'] div[data-testid='stPageLink']:first-of-type {{
        margin-top: 10px !important;
    }}

    [data-testid='stSidebar'] div[data-testid='stPageLink'],
    [data-testid='stSidebar'] div[data-testid='stPageLink'] > a,
    [data-testid='stSidebar'] div[data-testid='stPageLink'][aria-current="page"],
    [data-testid='stSidebar'] div[data-testid='stPageLink'][aria-current="page"] > a,
    [data-testid='stSidebar'] div[data-testid='stPageLink']:hover,
    [data-testid='stSidebar'] div[data-testid='stPageLink']:active,
    [data-testid='stSidebar'] div[data-testid='stPageLink']:focus {{
        background-color: #091326 !important;
        background-image: none !important;
        border: 1.5px solid #00bfff !important;
        border-radius: 6px !important;
        box-shadow: 0 0 14px rgba(0, 191, 255, 0.5), inset 0 0 6px rgba(0, 191, 255, 0.2) !important;
        margin-bottom: 6px !important;
        width: 100% !important;
        padding: 6px 8px !important;
        transform: none !important;
        opacity: 1 !important;
    }}
    
    [data-testid='stSidebar'] div[data-testid='stPageLink'] span,
    [data-testid='stSidebar'] div[data-testid='stPageLink'] p,
    [data-testid='stSidebar'] div[data-testid='stPageLink'] div {{
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 12px !important;
        background-color: transparent !important;
    }}

    .choose-category-title {{
        color: #0047ab !important;
        font-size: 14px !important;
        font-weight: 900 !important;
        letter-spacing: 1.2px !important;
        text-shadow: 0 0 10px rgba(0, 191, 255, 0.6), 0 0 20px rgba(0, 71, 171, 0.4) !important;
        margin-top: 12px !important;
        margin-bottom: 6px !important;
    }}

    .setting-section-title {{ color: {accent_color} !important; font-size: 15px !important; font-weight: 800 !important; margin-top: 12px !important; margin-bottom: 6px !important; }}
    </style>
    """


st.markdown(get_theme_css(st.session_state.app_theme), unsafe_allow_html=True)

# Sidebar Links
with st.sidebar:
    st.markdown(
        f"""
        <div style="margin-bottom: 0px;">
            <div style="display: flex; align-items: center; margin-bottom: 4px; padding-top: 0px;">
                {logo_img_tag}
                <span style="font-size: 16px; font-weight: 900; color: #ffffff; letter-spacing: 0.5px;">MAX </span>
                <span style="font-size: 16px; font-weight: 900; color: #00bfff; letter-spacing: 0.5px; text-shadow: 0 0 10px rgba(0, 191, 255, 0.7); margin-left: 4px;">Stem Splitter</span>
            </div>
            <div class="choose-category-title">CHOOSE CATEGORY</div>
        </div>
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

# Main Header (Back button paih bo a ni ta)
st.markdown(
    """
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 35px; margin-bottom: 15px;">
        <span style="font-size: 20px; font-weight: 800;">SETTINGS</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Settings Controls
st.markdown(
    '<div class="setting-section-title">🎨 Themes Appearance</div>',
    unsafe_allow_html=True,
)
st.selectbox(
    "Select Interface Theme:",
    ["Dark Mode (Default)", "Glassmorphic Dark", "Cyberpunk Blue Neon"],
    key="app_theme",
)

st.markdown(
    '<div class="setting-section-title">🎵 Audio Export Format & Quality</div>',
    unsafe_allow_html=True,
)
c1, c2 = st.columns(2)
with c1:
    st.selectbox(
        "Audio Format:", ["MP3", "WAV", "FLAC", "M4A"], key="export_format"
    )
with c2:
    st.selectbox(
        "Quality Bitrate:",
        ["320 kbps", "256 kbps", "192 kbps", "128 kbps"],
        key="export_bitrate",
    )

st.markdown(
    '<div class="setting-section-title">🚀 Processing Engine</div>',
    unsafe_allow_html=True,
)
st.selectbox(
    "Hardware Acceleration:",
    ["CPU (Default)", "GPU (CUDA Acceleration)"],
    key="processing_engine",
)

st.markdown(
    '<div class="setting-section-title">📁 Output Directory Path</div>',
    unsafe_allow_html=True,
)
st.text_input("Downloads Folder Path:", key="output_folder")

st.markdown(
    '<div class="setting-section-title">🧹 Maintenance & Storage</div>',
    unsafe_allow_html=True,
)
st.toggle("Automatically clean temporary files on exit", key="auto_cleanup")

st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
b1, b2, _ = st.columns([1, 1, 2])
with b1:
    if st.button("💾 Save Settings", use_container_width=True):
        current_config = {
            "app_theme": st.session_state.app_theme,
            "export_format": st.session_state.export_format,
            "export_bitrate": st.session_state.export_bitrate,
            "processing_engine": st.session_state.processing_engine,
            "output_folder": st.session_state.output_folder,
            "auto_cleanup": st.session_state.auto_cleanup,
        }
        if save_config(current_config):
            st.toast("Settings saved successfully!")
            st.rerun()
with b2:
    if st.button("🔄 Reset Defaults", use_container_width=True):
        for k, v in DEFAULT_SETTINGS.items():
            st.session_state[k] = v
        save_config(DEFAULT_SETTINGS)
        st.toast("Reset to default settings!")
        st.rerun()