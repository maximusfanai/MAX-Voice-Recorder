import base64
from datetime import datetime
import os
import time

import streamlit as st

st.set_page_config(
    page_title="MAX Cloud Drive",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Unified Theme & Styling
st.markdown(
    """
    <style>
    .stApp { background-color: #0b0c14 !important; color: #f1f5f9 !important; font-family: 'Segoe UI', sans-serif; }
    div[data-testid='stSidebarNav'] { display: none !important; }
    
    [data-testid='stSidebar'] {
        background-color: #090a10 !important;
        border-right: 1px solid #1c1e2d !important;
        max-width: 240px !important;
        min-width: 240px !important;
        padding-top: 0px !important;
    }

    /* << leh >> Icons hnuai lama sawnhniam belhna */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"],
    div[data-testid="stSidebarHeader"] {
        margin-top: 35px !important;
        padding-top: 10px !important;
        transform: translateY(15px) !important;
    }
    
    /* MAX Stem Splitter & CHOOSE CATEGORY */
    [data-testid='stSidebar'] > div:first-child {
        padding-top: 0px !important;
        margin-top: -70px !important;
    }

    [data-testid='stSidebar'] [data-testid='stVerticalBlock'] {
        gap: 8px !important;
    }

    /* HOMEPAGE atanga SETTINGS thleng hnuai lama sawnhniamna */
    [data-testid='stSidebar'] div[data-testid='stPageLink']:first-of-type {
        margin-top: 18px !important;
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

    /* Main Content Area - A title leh content zawng zawng fiah taka lang kim tura hnuai lama sawn thlakna */
    div[data-testid="stMainBlockContainer"],
    .main .block-container {
        padding-top: 40px !important;
        margin-top: 0px !important;
    }

    /* Input Styling matching design */
    div[data-testid='stTextInput'] {
        width: 100% !important;
        margin-bottom: 0px !important;
    }

    div[data-testid='stTextInput'] label {
        font-size: 13px !important;
        font-weight: 600 !important;
        color: #94a3b8 !important;
        margin-bottom: 6px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
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

    .status-badge-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #161929;
        border: 1.5px solid #25283d;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
    }
    .status-active {
        color: #10b981;
        font-weight: bold;
        font-size: 13px;
    }

    .file-item-card {
        background-color: #161929;
        border: 1.5px solid #25283d;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    
    .file-title {
        color: #ffffff;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 4px;
    }
    
    .file-meta {
        color: #94a3b8;
        font-size: 12px;
        font-weight: 500;
    }

    /* Buttons Fix */
    div[data-testid="stButton"] button,
    div[data-testid="stDownloadButton"] button,
    div.stButton > button,
    div.stDownloadButton > button { 
        background: linear-gradient(135deg, #06b6d4 0%, #0284c7 100%) !important; 
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 10px 16px !important;
        box-shadow: 0 4px 14px rgba(6, 182, 212, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-top: 10px !important;
        font-size: 14px !important;
    }

    details summary div[data-testid="stExpanderToggleIcon"],
    summary svg[data-testid="stExpanderToggleIcon"] {
        display: none !important;
    }
    
    div[data-testid='InputInstructions'] { display: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Local logo path
logo_path = r"E:\stemsplitterproject\assets\logo.png"
if not os.path.exists(logo_path):
    if os.path.exists(r"E:\stemsplitterproject\assets\logo"):
        logo_path = r"E:\stemsplitterproject\assets\logo"

logo_img_tag = ""
if os.path.exists(logo_path):
    try:
        with open(logo_path, "rb") as f:
            encoded_logo = base64.b64encode(f.read()).decode("utf-8")
            logo_img_tag = f'<img src="data:image/png;base64,{encoded_logo}" style="height: 24px; width: auto; margin-right: 8px; vertical-align: middle;" />'
    except Exception as e:
        print(f"Error loading logo: {e}")

# Sidebar Header
with st.sidebar:
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; margin-bottom: 4px; padding-top: 0px;">
            {logo_img_tag}
            <span style="font-size: 16px; font-weight: 900; color: #ffffff; letter-spacing: 0.5px;">MAX </span>
            <span style="font-size: 16px; font-weight: 900; color: #00bfff; letter-spacing: 0.5px; text-shadow: 0 0 10px rgba(0, 191, 255, 0.7); margin-left: 4px;">Stem Splitter</span>
        </div>
        <div style="color: #00bfff; font-size: 11px; font-weight: 900; margin-bottom: 12px; letter-spacing: 1px;">CHOOSE CATEGORY</div>
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

# ==========================================
# CUSTOM MAIN TITLE 
# ==========================================
st.markdown(
    """
    <div style="display: flex; align-items: center; margin-bottom: 4px;">
        <span style="color: #ffffff; font-size: 20px; font-weight: 900; letter-spacing: 0.5px;">CLOUD DRIVE</span>
    </div>
    <div style="color: #94a3b8; font-size: 11px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 24px;">
        ☁️ CLOUD STORAGE & BACKUP
    </div>
    """,
    unsafe_allow_html=True,
)

cloud_dir = "cloud_drive"
os.makedirs(cloud_dir, exist_ok=True)

def get_file_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"

# Storage Bar
files_list = []
for root, dirs, filenames in os.walk(cloud_dir):
    for f in filenames:
        files_list.append(os.path.join(root, f))

total_used_bytes = sum(os.path.getsize(f) for f in files_list if os.path.exists(f))
used_mb = total_used_bytes / (1024 * 1024)
max_quota_mb = 1024.0
quota_pct = min(int((used_mb / max_quota_mb) * 100), 100)

st.markdown(
    f"""
    <div class="status-badge-container">
        <div>
            <div class="status-active">🟢 MAX Local Cloud Sync Active</div>
            <div style="font-size:12px; color:#94a3b8; margin-top:2px;">Storage Folder: <code>./cloud_drive/</code></div>
        </div>
        <div style="text-align:right;">
            <div style="font-size:13px; font-weight:bold; color:#06b6d4;">{used_mb:.1f} MB / {max_quota_mb:.0f} MB Used</div>
            <div style="font-size:11px; color:#94a3b8;">Quota Used: {quota_pct}%</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.progress(quota_pct / 100, text=f"Storage Capacity: {quota_pct}%")

st.markdown("<br>", unsafe_allow_html=True)

# Gallery Backup / Batch Selector Section
with st.expander(
    "📸 Gallery Backup: Select Files & Create Custom Folder", expanded=True
):
    st.markdown(
        "<div style='font-size:13px; color:#94a3b8; margin-bottom:12px; font-weight:500;'>Hmun hrang hranga i file siam tawhte (Outputs, Voice Records, Projects) lo lang chu tick-in, folder bik siamin a rualin backup rawh.</div>",
        unsafe_allow_html=True,
    )

    source_dirs = ["output", "voice_records", "stemtube_downloads"]
    all_source_files = []

    for sdir in source_dirs:
        if os.path.exists(sdir):
            for root, dirs, files in os.walk(sdir):
                for file in files:
                    f_path = os.path.join(root, file)
                    all_source_files.append(
                        {
                            "name": file,
                            "path": f_path,
                            "size": os.path.getsize(f_path),
                            "mtime": os.path.getmtime(f_path),
                            "category": sdir,
                        }
                    )

    if not all_source_files:
        st.info(
            "Backup tur file hmuh tur a la awm lo. Stem Splitter emaw Voice"
            " Recorder-ah file siam hmasa phawt rawh."
        )
    else:
        backup_folder_name = st.text_input(
            "📁 Cloud Backup Folder Hming (Optional):",
            value="My_Backup",
            placeholder="Entirnan: Album_1, Jam_Tracks",
        )

        selected_files_to_backup = []

        st.markdown(
            "<div style='font-size:13px; font-weight:600; color:#ffffff; margin-top:16px; margin-bottom:8px; text-transform:uppercase; letter-spacing:0.5px;'>Select Files to Backup:</div>",
            unsafe_allow_html=True,
        )

        for idx, sf in enumerate(all_source_files):
            col_chk, col_info = st.columns([0.1, 0.9])
            with col_chk:
                is_checked = st.checkbox("", key=f"sel_file_{idx}")
            with col_info:
                st.markdown(
                    f"<div style='padding-top: 4px;'><strong style='color:#ffffff; font-size:13px;'>{sf['name']}</strong> <span style='font-size:11px; color:#94a3b8;'>({sf['category']} | {get_file_size(sf['size'])})</span></div>",
                    unsafe_allow_html=True,
                )
                if is_checked:
                    selected_files_to_backup.append(sf)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Backup Selected Files to Cloud", use_container_width=True):
            if not selected_files_to_backup:
                st.warning("Backup tur file pakhat mah i la tick lo!")
            else:
                target_sub_dir = os.path.join(
                    cloud_dir, backup_folder_name.strip() or "General"
                )
                os.makedirs(target_sub_dir, exist_ok=True)

                copied_count = 0
                for item in selected_files_to_backup:
                    dest_path = os.path.join(target_sub_dir, item["name"])
                    with open(item["path"], "rb") as f_src, open(
                        dest_path, "wb"
                    ) as f_dst:
                        f_dst.write(f_src.read())
                    copied_count += 1

                st.success(
                    f"Successfully backed up {copied_count} file(s) to folder:"
                    f" '{backup_folder_name}'!"
                )
                time.sleep(1)
                st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# List Cloud Files & Folders
st.markdown(
    '<div style="font-size:13px; color:#06b6d4; font-weight:700; margin-bottom:12px; text-transform:uppercase; letter-spacing:0.5px;">Cloud Drive Contents & Folders</div>',
    unsafe_allow_html=True,
)

root_files = [
    f for f in os.listdir(cloud_dir) if os.path.isfile(os.path.join(cloud_dir, f))
]
root_dirs = [
    d for d in os.listdir(cloud_dir) if os.path.isdir(os.path.join(cloud_dir, d))
]

if not root_files and not root_dirs:
    st.markdown(
        """
        <div style="background-color:#161929; border:1.5px dashed #25283d; border-radius:12px; padding:30px; text-align:center; color:#94a3b8; font-size:13px;">
            <div style="font-size:32px; margin-bottom:8px;">☁️</div>
            <div style="font-weight: 700; color: #ffffff; margin-bottom: 4px;">Cloud Storage is empty.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    if root_dirs:
        st.markdown(
            "<div style='font-size:12px; color:#94a3b8; font-weight:700; margin-bottom:8px; text-transform:uppercase; letter-spacing:0.5px;'>FOLDERS</div>",
            unsafe_allow_html=True,
        )
        for folder_name in root_dirs:
            folder_path = os.path.join(cloud_dir, folder_name)
            sub_files = os.listdir(folder_path)
            st.markdown(
                f"""
                <div class="file-item-card" style="border-left: 4px solid #06b6d4;">
                    <div class="file-title">📁 {folder_name}</div>
                    <div class="file-meta">Contains {len(sub_files)} file(s)</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if root_files:
        st.markdown(
            "<div style='font-size:12px; color:#94a3b8; font-weight:700; margin-top:16px; margin-bottom:8px; text-transform:uppercase; letter-spacing:0.5px;'>FILES</div>",
            unsafe_allow_html=True,
        )
        for idx, fname in enumerate(root_files):
            fpath = os.path.join(cloud_dir, fname)
            stat = os.stat(fpath)
            mod_time = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
            size_str = get_file_size(stat.st_size)

            st.markdown(
                f"""
                <div class="file-item-card">
                    <div class="file-title">☁️ {fname}</div>
                    <div class="file-meta">Uploaded: {mod_time} &nbsp;|&nbsp; Size: {size_str}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            c_play, c_dl, c_del = st.columns([4, 2, 1.5])
            with c_play:
                if fname.lower().endswith((".mp3", ".wav", ".m4a", ".flac", ".ogg")):
                    st.audio(fpath)
                else:
                    st.markdown("<div style='margin-top:10px; color:#94a3b8; font-size:13px;'>📄 Non-media file</div>", unsafe_allow_html=True)
            with c_dl:
                with open(fpath, "rb") as fd:
                    st.download_button(
                        "💾 Download", fd, file_name=fname, key=f"dl_root_{idx}", use_container_width=True
                    )
            with c_del:
                if st.button("🗑️ Delete", key=f"del_root_{idx}", use_container_width=True):
                    os.remove(fpath)
                    st.toast(f"Removed {fname}")
                    time.sleep(0.3)
                    st.rerun()