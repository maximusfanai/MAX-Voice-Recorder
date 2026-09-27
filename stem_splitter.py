import base64
import io
import os
import threading
import time
import numpy as np
import soundfile as sf
import streamlit as st


# Demucs Model RAM-a Cache Tura Function (Vawikhat chiah a load tawh ang)
@st.cache_resource
def load_demucs_model():
  import torch
  from demucs.pretrained import get_model

  device = "cuda" if torch.cuda.is_available() else "cpu"
  model = get_model("htdemucs")
  model.to(device)
  model.eval()
  return model, device


# Local PC / Device-a folder thlan tura Tkinter popup
def choose_folder():
  try:
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    folder_selected = filedialog.askdirectory(master=root)
    root.destroy()
    return folder_selected
  except Exception:
    return None


# Load logo image as base64 for sidebar (ti te zawk - 24px)
def get_img_as_base64(file_path):
  if os.path.exists(file_path):
    with open(file_path, "rb") as f:
      data = f.read()
    return base64.b64encode(data).decode()
  return ""


logo_path = "assets/logo.png"
if not os.path.exists(logo_path) and os.path.exists("../assets/logo.png"):
  logo_path = "../assets/logo.png"
logo_b64 = get_img_as_base64(logo_path)
logo_html = (
    f'<img src="data:image/png;base64,{logo_b64}" style="width: 32px; height: 32px; object-fit: contain; vertical-align: middle; margin-right: 8px;" />'
    if logo_b64
    else ""
)

# Phone-a Portrait-a hmeh din tura JavaScript
st.markdown(
    """
    <script>
    function triggerPortrait() {
        let elem = document.documentElement;
        if (elem.requestFullscreen) {
            elem.requestFullscreen().then(() => {
                if (screen.orientation && screen.orientation.lock) {
                    screen.orientation.lock('portrait').catch(function(error) {
                        console.log("Orientation lock failed: ", error);
                    });
                }
            }).catch(function(err) {
                console.log("Fullscreen request failed: ", err);
            });
        }
    }
    </script>
    
    <style>
    html, body, .stApp { 
        background-color: #080914 !important; 
        color: #f1f5f9 !important; 
        font-family: 'Segoe UI', system-ui, sans-serif !important;
        overflow-x: hidden !important;
    }
    
    div[data-testid='stSidebarNav'] { display: none !important; }
    
    [data-testid='stSidebar'] { 
        background-color: #06070d !important; 
        border-right: 1px solid #1a1c2e !important;
        max-width: 230px !important;
        min-width: 230px !important;
        padding-top: 0px !important;
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

    .choose-category-title {
        color: #0044ff !important;
        font-size: 15px !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px !important;
        margin-top: 10px !important;
        margin-bottom: 10px !important;
        text-shadow: 0 0 10px rgba(0, 68, 255, 0.7), 0 0 20px rgba(0, 68, 255, 0.4) !important;
    }

    .block-container { 
        max-width: 100% !important; 
        padding: 0.5rem 0.8rem !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"],
    [data-testid="stFileUploaderDropzoneInstructions"] *,
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] section > div > div > span {
        display: none !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin-bottom: 4px !important;
        pointer-events: none !important;
    }

    [data-testid="stFileUploaderDropzone"] button {
        background: linear-gradient(135deg, #021a2e 0%, #032d4a 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        border-radius: 8px !important;
        border: 1.5px solid #00bfff !important;
        box-shadow: 0 0 15px rgba(0, 191, 255, 0.4), inset 0 0 10px rgba(0, 191, 255, 0.15) !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        padding: 8px 18px !important;
        transition: all 0.2s ease-in-out !important;
        pointer-events: auto !important;
    }

    [data-testid="stFileUploaderDropzone"] button:active,
    [data-testid="stFileUploaderDropzone"] button:focus,
    [data-testid="stFileUploaderDropzone"] button[data-baseweb="button"]:active {
        background: #010c14 !important;
        background-color: #010c14 !important;
        color: #ffffff !important;
        border-color: #38bdf8 !important;
        box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.9), 0 0 18px rgba(56, 189, 248, 0.8) !important;
    }

    [data-testid="stFileUploaderDropzone"] button:hover {
        background: linear-gradient(135deg, #032640 0%, #043c63 100%) !important;
        color: #ffffff !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.6), inset 0 0 12px rgba(56, 189, 248, 0.3) !important;
    }

    [data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] > div {
        border: 1.5px solid rgba(0, 191, 255, 0.6) !important;
        border-radius: 10px !important;
        background: rgba(4, 13, 26, 0.75) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        padding: 10px !important;
        box-shadow: 0 0 20px rgba(0, 191, 255, 0.25), inset 0 0 15px rgba(0, 191, 255, 0.08) !important;
        pointer-events: none !important;
    }

    audio {
        width: 100% !important;
        height: 32px !important;
        border-radius: 16px !important;
    }
    
    div[data-testid="stAudio"] {
        width: 100% !important;
        margin-top: 4px !important;
        margin-bottom: 6px !important;
    }

    div[data-testid="stButton"] button { 
        background: linear-gradient(135deg, #022c43 0%, #034f75 100%) !important; 
        border-radius: 8px !important; 
        border: 1.5px solid #38bdf8 !important; 
        color: #ffffff !important; 
        font-weight: bold !important;
        font-size: 11px !important;
        height: 34px !important;
        width: 120px !important;
        max-width: 100% !important;
        display: block !important;
        margin: 0 auto !important;
        box-shadow: 0 0 16px rgba(56, 189, 248, 0.4), inset 0 0 8px rgba(56, 189, 248, 0.2) !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
    }

    div[data-testid="stButton"] button:hover {
        background: linear-gradient(135deg, #033c5c 0%, #04689c 100%) !important;
        border-color: #00bfff !important;
        box-shadow: 0 0 22px rgba(0, 191, 255, 0.7), inset 0 0 12px rgba(0, 191, 255, 0.4) !important;
    }

    .sec-title-blue {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 20px !important;
        letter-spacing: 0.5px;
        margin-top: 12px !important;
        margin-bottom: 6px !important;
        text-transform: uppercase;
    }

    .stem-item-title {
        color: #38bdf8 !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-top: 10px !important;
        margin-bottom: 4px !important;
    }

    .stExpander {
        background: linear-gradient(135deg, #021a2e 0%, #032d4a 100%) !important;
        border: 1.5px solid #00bfff !important;
        border-radius: 6px !important;
        box-shadow: 0 0 12px rgba(0, 191, 255, 0.3), inset 0 0 8px rgba(0, 191, 255, 0.1) !important;
        margin-bottom: 8px !important; 
        max-width: 200px !important;
        min-width: 200px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    .stExpander summary {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 11px !important;
        padding-top: 6px !important;
        padding-bottom: 6px !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
        min-height: 32px !important;
    }

    .stExpander [data-testid="stExpanderDetails"] {
        padding-top: 2px !important;
        padding-bottom: 6px !important;
        padding-left: 8px !important;
        padding-right: 8px !important;
    }

    .stExpander [data-testid="stSlider"] {
        margin-bottom: -6px !important;
        margin-top: 2px !important;
    }

    div[data-testid="stRadio"] label p, div[data-testid="stRadio"] label span {
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 800 !important;
    }

    .stExpander [data-testid="stRadio"] {
        margin-bottom: 8px !important;
        margin-top: 8px !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

if "output_folder" not in st.session_state:
  st.session_state.output_folder = "downloads"
if "split_done" not in st.session_state:
  st.session_state.split_done = False
if "splitting_in_progress" not in st.session_state:
  st.session_state.splitting_in_progress = False
if "stem_tensors" not in st.session_state:
  st.session_state.stem_tensors = {}
if "sample_rate" not in st.session_state:
  st.session_state.sample_rate = 44100
if "last_uploaded_file_name" not in st.session_state:
  st.session_state.last_uploaded_file_name = None
if "expander_open" not in st.session_state:
  st.session_state.expander_open = False

with st.sidebar:
  st.markdown(
      f"""
        <div style="padding-top: 0px; margin-top: -65px;">
            <div style="font-size: 14px; font-weight: 900; color: #ffffff; letter-spacing: 0.5px; margin-bottom: 2px; line-height: 1.2; display: flex; align-items: center;">
                {logo_html}<span><span style="color: #ffffff; text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);">MAX</span> <span style="color: #38bdf8; text-shadow: 0 0 10px rgba(56, 189, 248, 0.8);">Stem Splitter</span></span>
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

st.markdown(
    '<div style="font-weight:900; font-size:22px; color:#ffffff; margin-bottom:8px; display: flex; align-items: center;">'
    f'{logo_html}<span style="color: #ffffff; text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);">MAX</span>&nbsp;<span style="color: #38bdf8; text-shadow: 0 0 10px rgba(56, 189, 248, 0.8), 0 0 20px rgba(56, 189, 248, 0.4);">Stem Splitter</span>&nbsp;<span style="color:#ffffff; font-weight:normal; font-size:18px;">| Stem Splitter</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sec-title-blue">🎛️ STEM SPLITTER</div>', unsafe_allow_html=True
)

col_left, col_right = st.columns([0.72, 0.28], gap="small")

with col_right:
  st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

with col_left:
  st.markdown(
      '<div class="sec-title-blue">SELECT AUDIO</div>', unsafe_allow_html=True
  )

  uploaded_file = st.file_uploader(
      "Upload Audio", type=["mp3", "wav"], label_visibility="collapsed"
  )

  if uploaded_file is not None:
    if st.session_state.last_uploaded_file_name != uploaded_file.name:
      st.session_state.last_uploaded_file_name = uploaded_file.name
      st.session_state.split_done = False
      st.session_state.stem_tensors = {}

    if (
        not st.session_state.splitting_in_progress
        and not st.session_state.split_done
    ):
      st.audio(uploaded_file, format="audio/wav")

  # Callback function to handle selection and auto-close expander
  def on_quality_change():
    st.session_state.expander_open = False

  with st.expander(
      "⚡ SEPARATION QUALITY", expanded=st.session_state.expander_open
  ):
    separation_quality = st.radio(
        "Quality",
        ["Fast", "Normal", "High", "Ultra"],
        index=2,
        label_visibility="collapsed",
        key="separation_quality_radio",
        on_change=on_quality_change,
    )

  _, btn_col, _ = st.columns([1, 2, 1])
  with btn_col:
    button_label = (
        "Cancel" if st.session_state.splitting_in_progress else "✂️ SPLITTER"
    )
    if st.button(button_label, use_container_width=True):
      if uploaded_file is not None:
        if not st.session_state.splitting_in_progress:
          st.markdown(
              '<script>triggerPortrait();</script>',
              unsafe_allow_html=True,
          )
          st.session_state.splitting_in_progress = True
          st.rerun()
        else:
          st.session_state.splitting_in_progress = False
          st.session_state.split_done = False
          st.session_state.stem_tensors = {}
          st.rerun()
      else:
        st.warning("Please upload an audio file first!")

  if (
      uploaded_file is not None
      and st.session_state.splitting_in_progress
      and not st.session_state.split_done
  ):
    progress_text = st.empty()
    my_bar = st.progress(0)

    try:
      # 1% - 15%: Model Loading
      for p in range(1, 16):
        if not st.session_state.splitting_in_progress:
          st.rerun()
        my_bar.progress(p)
        progress_text.markdown(
            f"<div style='color: #00bfff; font-weight: bold; text-align: center; margin-bottom: 5px;'>Loading Model... {p}%</div>",
            unsafe_allow_html=True,
        )
        time.sleep(0.04)

      model, device = load_demucs_model()

      if not st.session_state.splitting_in_progress:
        st.rerun()

      # 16% - 35%: Audio Reading & Conversion
      audio_bytes_data = uploaded_file.read()
      data, sr = sf.read(io.BytesIO(audio_bytes_data))

      if len(data.shape) == 1:
        data = np.stack([data, data], axis=0)
      else:
        data = data.T

      import torch
      from demucs.audio import convert_audio

      wav = torch.from_numpy(data).float()
      target_sr = 44100
      wav = convert_audio(wav, sr, target_sr, model.audio_channels)

      for p in range(16, 36):
        if not st.session_state.splitting_in_progress:
          st.rerun()
        my_bar.progress(p)
        progress_text.markdown(
            f"<div style='color: #00bfff; font-weight: bold; text-align: center; margin-bottom: 5px;'>Processing Audio ({separation_quality} Mode)... {p}%</div>",
            unsafe_allow_html=True,
        )
        time.sleep(0.03)

      if not st.session_state.splitting_in_progress:
        st.rerun()

      # Setup Demucs parameters
      ref = wav.mean(0)
      wav = (wav - ref.mean()) / ref.std()

      if separation_quality == "Fast":
        shifts = 0
        overlap = 0.1
      elif separation_quality == "Normal":
        shifts = 1
        overlap = 0.25
      elif separation_quality == "High":
        shifts = 2
        overlap = 0.5
      else:
        shifts = 3
        overlap = 0.75

      # 36% - 85%: Background AI Separation with smooth active progress counter
      result_holder = {}

      def run_demucs():
        try:
          import torch
          from demucs.apply import apply_model

          with torch.no_grad():
            res = apply_model(
                model,
                wav[None],
                shifts=shifts,
                overlap=overlap,
                device=device,
            )[0]
            result_holder["sources"] = res
        except Exception as ex:
          result_holder["error"] = ex

      thread = threading.Thread(target=run_demucs)
      thread.start()

      curr_p = 36
      while thread.is_alive():
        if not st.session_state.splitting_in_progress:
          st.rerun()
        if curr_p < 85:
          curr_p += 1
          my_bar.progress(curr_p)
          progress_text.markdown(
              f"<div style='color: #00bfff; font-weight: bold; text-align: center; margin-bottom: 5px;'>Isolating Stems ({separation_quality} - {device.upper()})... {curr_p}%</div>",
              unsafe_allow_html=True,
          )
        time.sleep(0.12)

      thread.join()

      if "error" in result_holder:
        raise result_holder["error"]

      sources = result_holder["sources"]
      sources = sources * ref.std() + ref.mean()

      # 86% - 100%: Extract stems & finalize smoothly
      sources_names = model.sources
      st.session_state.stem_tensors = {}
      for i, name in enumerate(sources_names):
        st.session_state.stem_tensors[name] = sources[i].detach().cpu().numpy()

      st.session_state.sample_rate = target_sr

      for p in range(curr_p, 100):
        if not st.session_state.splitting_in_progress:
          st.rerun()
        my_bar.progress(p + 1)
        progress_text.markdown(
            f"<div style='color: #00bfff; font-weight: bold; text-align: center; margin-bottom: 5px;'>Finalizing Stems... {p + 1}%</div>",
            unsafe_allow_html=True,
        )
        time.sleep(0.02)

      progress_text.markdown(
          "<div style='color: #22c55e; font-weight: 900; text-align: center; margin-bottom: 5px;'>Complete! 100%</div>",
          unsafe_allow_html=True,
      )
      time.sleep(0.4)
      st.session_state.split_done = True
      st.session_state.splitting_in_progress = False
      st.rerun()

    except Exception as e:
      st.error(f"Error during splitting: {e}")
      st.session_state.splitting_in_progress = False

  @st.fragment
  def render_stems_output():
    if st.session_state.split_done and len(st.session_state.stem_tensors) > 0:
      st.markdown(
          '<div class="sec-title-blue">STEM TO EXTRACT</div>',
          unsafe_allow_html=True,
      )

      stems_list = [
          {"name": "Vocals", "icon": "🎤", "key": "vocals"},
          {"name": "Drum", "icon": "🥁", "key": "drums"},
          {"name": "Bass", "icon": "🎸", "key": "bass"},
          {"name": "Other Instrument", "icon": "🎹", "key": "other"},
          {
              "name": "Track (bass, drum, instruments)",
              "icon": "🎼",
              "key": "track_mix",
          },
      ]

      for item in stems_list:
        st.markdown(
            f'<div class="stem-item-title"><span>{item["icon"]}</span><span>{item["name"]}</span></div>',
            unsafe_allow_html=True,
        )

        try:
          sr = st.session_state.sample_rate
          if item["key"] == "track_mix":
            d = st.session_state.stem_tensors.get("drums", np.zeros((2, 1)))
            b = st.session_state.stem_tensors.get("bass", np.zeros((2, 1)))
            o = st.session_state.stem_tensors.get("other", np.zeros((2, 1)))
            combined = d + b + o
            audio_data = combined.T
          else:
            tensor_data = st.session_state.stem_tensors.get(
                item["key"], np.zeros((2, 1))
            )
            audio_data = tensor_data.T

          io_buf = io.BytesIO()
          sf.write(io_buf, audio_data, sr, format="WAV")
          io_buf.seek(0)
          stem_bytes = io_buf.read()
          mime_type = "audio/wav"
        except Exception:
          stem_bytes = uploaded_file.getvalue() if uploaded_file else b""
          mime_type = "audio/wav"

        st.audio(stem_bytes, format=mime_type)

        # BUTTON TEXT-A AN HMING PAIH A NI TA (📥 Download chiah)
        dl_clicked = st.button("📥 Download", key=f"dl_btn_{item['key']}")
        
        state_key = f"download_triggered_{item['key']}"
        if dl_clicked:
          st.session_state[state_key] = True

        if st.session_state.get(state_key, False):
          ad_box = st.empty()
          for sec in range(15, 0, -1):
            ad_box.markdown(
                f"""
                <div style="background: #111; border: 1.5px solid #38bdf8; padding: 15px; border-radius: 10px; text-align: center; margin: 10px 0; box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);">
                    <p style="color: #38bdf8; font-weight: bold; margin: 0; font-size: 13px;">📺 Sponsored Ad ({item['name']} Download)...</p>
                    <h2 style="color: #ffcc00; font-weight: 900; margin: 5px 0 0 0; font-size: 30px;">{sec}s</h2>
                </div>
                """,
                unsafe_allow_html=True,
            )
            time.sleep(1)
          ad_box.empty()
          
          st.session_state[state_key] = False
          st.download_button(
              label="💾 Click to save",
              data=stem_bytes,
              file_name=f"{item['key']}_stem.wav",
              mime=mime_type,
              key=f"auto_dl_save_{item['key']}",
              use_container_width=True
          )

  render_stems_output()