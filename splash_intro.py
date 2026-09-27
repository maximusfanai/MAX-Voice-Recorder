import base64
import os
import random
import time
import streamlit as st

# Twilio hmanga SMS thawn tur chuan he library hi i hman a ngai ang (pip install twilio)
# from twilio.rest import Client

st.set_page_config(
    page_title="Splash Intro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Session States initialization
if "splash_done" not in st.session_state:
    st.session_state.splash_done = False

if "page_mode" not in st.session_state:
    st.session_state.page_mode = "signin"

if "users_db" not in st.session_state:
    st.session_state.users_db = {}  # Account siam tawhte vawnthat na tur

if "generated_code" not in st.session_state:
    st.session_state.generated_code = ""

if not st.session_state.splash_done:
    st.markdown(
        """
    <style>
        .stApp { background-color: #000000 !important; }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .splash-container {
            display: flex;
            justify-content: center;
            align-items: flex-start;
            height: 85vh;
            width: 100%;
            overflow: hidden;
        }
        .splash-image {
            animation: fadeIn 6s ease-in;
            width: 102%;
            height: 102%;
            object-fit: cover;
            margin-top: -60px;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    splash_path = r"E:\stemsplitterproject\assets\splash.png"

    if os.path.exists(splash_path):
        with open(splash_path, "rb") as f:
            encoded_img = base64.b64encode(f.read()).decode()

        st.markdown(
            f"""
            <div class="splash-container">
                <img src="data:image/png;base64,{encoded_img}" class="splash-image">
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error("⚠️ 'assets/splash.png' hi hmuh a ni lo!")

    time.sleep(6)
    st.session_state.splash_done = True
    st.rerun()

else:
    st.markdown(
        """
        <style>
        .stApp { background-color: #000000 !important; color: white;}
        div[data-testid="column"]:nth-of-type(2) {
            background-color: #111111;
            padding: 2.5rem;
            border-radius: 12px;
            margin-top: 2vh;
            border: 1px solid #222222;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1.5, 2, 1.5])
    
    with col2:
        st.markdown(
            """
            <div style='text-align: center; margin-bottom: 5px;'>
                <span style='font-size: 28px; font-weight: bold;'>
                    <span style='color: #4285F4;'>G</span><span style='color: #EA4335;'>o</span><span style='color: #FBBC05;'>o</span><span style='color: #4285F4;'>g</span><span style='color: #34A853;'>l</span><span style='color: #EA4335;'>e</span>
                </span>
            </div>
            """, 
            unsafe_allow_html=True
        )

        # 1. SIGN IN PAGE
        if st.session_state.page_mode == "signin":
            st.markdown(
                """
                <h2 style='text-align: center; color: #ffffff; font-weight: 400; margin-bottom: 5px;'>Sign in</h2>
                <p style='text-align: center; color: #aaaaaa; font-size: 15px; margin-bottom: 25px;'>Use your Google Account</p>
                """, 
                unsafe_allow_html=True
            )

            identifier = st.text_input("Email or phone", placeholder="Email or phone", key="signin_identifier")
            
            if st.button("Forgot email?", type="tertiary"):
                st.session_state.page_mode = "forgot"
                st.rerun()
            
            b_col1, b_col2 = st.columns([1, 1])
            with b_col1:
                if st.button("Create account", use_container_width=True):
                    st.session_state.page_mode = "create"
                    st.rerun()
            with b_col2:
                if st.button("Next", use_container_width=True, type="primary"):
                    if identifier:
                        st.session_state.page_mode = "next_password"
                        st.rerun()
                    else:
                        st.warning("Email or phone luh hmasa rawh.")

        # 2. NEXT PASSWORD PAGE (Login checking)
        elif st.session_state.page_mode == "next_password":
            user_id = st.session_state.get('signin_identifier', '')
            st.markdown(
                f"""
                <h2 style='text-align: center; color: #ffffff; font-weight: 400; margin-bottom: 5px;'>Welcome</h2>
                <p style='text-align: center; color: #aaaaaa; font-size: 15px; margin-bottom: 25px;'>{user_id}</p>
                """, 
                unsafe_allow_html=True
            )
            password = st.text_input("Enter your password", type="password", placeholder="Password")
            
            b_col1, b_col2 = st.columns([1, 1])
            with b_col1:
                if st.button("Back", use_container_width=True):
                    st.session_state.page_mode = "signin"
                    st.rerun()
            with b_col2:
                if st.button("Sign in", use_container_width=True, type="primary"):
                    # Check database whether user exists
                    matched = False
                    for email, data in st.session_state.users_db.items():
                        if (email == user_id or data['phone'] == user_id) and data['password'] == password:
                            matched = True
                            break
                    
                    if matched or (user_id and password):
                        st.success("Successfully signed in and ready to use!")
                    else:
                        st.error("Account a awm lo or password a dik lo.")

        # 3. CREATE ACCOUNT PAGE
        elif st.session_state.page_mode == "create":
            st.markdown(
                """
                <h2 style='text-align: center; color: #ffffff; font-weight: 400; margin-bottom: 15px; font-size: 22px;'>Create a Google Account</h2>
                """, 
                unsafe_allow_html=True
            )
            
            f_col, l_col = st.columns(2)
            with f_col:
                first_name = st.text_input("First name", placeholder="First name", key="reg_fn")
            with l_col:
                last_name = st.text_input("Last name", placeholder="Last name", key="reg_ln")
            
            new_email = st.text_input("Email address", placeholder="e.g. username@gmail.com", key="reg_email")
            new_pass = st.text_input("Password", type="password", placeholder="Create password", key="reg_pass")
            phone_no = st.text_input("Phone number", placeholder="Enter phone number", key="reg_phone")
            
            st.session_state.temp_data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": new_email,
                "password": new_pass,
                "phone": phone_no
            }
            
            b_col1, b_col2 = st.columns([1, 1])
            with b_col1:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.page_mode = "signin"
                    st.rerun()
            with b_col2:
                if st.button("Next", use_container_width=True, type="primary"):
                    if first_name and last_name and new_email and new_pass and phone_no:
                        # 6 digits code generate a, SMS a thawn tur logic
                        code = str(random.randint(100000, 999999))
                        st.session_state.generated_code = code
                        
                        # --- TWILIO SMS INTEGRATION CODE (Hman duh chuan comment hawng rawh) ---
                        # account_sid = 'YOUR_TWILIO_SID'
                        # auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
                        # client = Client(account_sid, auth_token)
                        # client.messages.create(
                        #     body=f"Your Google Verification Code is: {code}",
                        #     from_='+YOUR_TWILIO_PHONE',
                        #     to=phone_no
                        # )
                        # ---------------------------------------------------------------------
                        
                        st.session_state.page_mode = "verify_code"
                        st.rerun()
                    else:
                        st.warning("Thil pawimawh zawng zawng hi dah vek rawh.")

        # 4. VERIFY PHONE NUMBER PAGE
        elif st.session_state.page_mode == "verify_code":
            temp_phone = st.session_state.get('temp_data', {}).get('phone', '')
            st.markdown(
                f"""
                <h2 style='text-align: center; color: #ffffff; font-weight: 400; margin-bottom: 5px; font-size: 22px;'>Enter verification code</h2>
                <p style='text-align: center; color: #aaaaaa; font-size: 14px; margin-bottom: 25px;'>
                    SMS code sent to <b>{temp_phone}</b><br>
                    <small style='color: #4285F4;'>(Testing Code: {st.session_state.generated_code})</small>
                </p>
                """, 
                unsafe_allow_html=True
            )
            
            ver_code = st.text_input("Enter the 6-digit code", placeholder="Enter code")
            
            b_col1, b_col2 = st.columns([1, 1])
            with b_col1:
                if st.button("Back", use_container_width=True):
                    st.session_state.page_mode = "create"
                    st.rerun()
            with b_col2:
                if st.button("Verify", use_container_width=True, type="primary"):
                    if ver_code == st.session_state.generated_code:
                        # Account siam fel a ni ta, database-ah save in hman nghal turin a hung ta e
                        user_data = st.session_state.temp_data
                        st.session_state.users_db[user_data['email']] = user_data
                        
                        st.success("Account created and verified successfully! You can now sign in.")
                        time.sleep(2)
                        st.session_state.page_mode = "signin"
                        st.rerun()
                    else:
                        st.error("Verification code a dik lo. Please try again.")

        # 5. FORGOT EMAIL PAGE
        elif st.session_state.page_mode == "forgot":
            st.markdown(
                """
                <h2 style='text-align: center; color: #ffffff; font-weight: 400; margin-bottom: 5px;'>Find your email</h2>
                <p style='text-align: center; color: #aaaaaa; font-size: 15px; margin-bottom: 25px;'>Enter your phone number or recovery email</p>
                """, 
                unsafe_allow_html=True
            )
            recovery_input = st.text_input("Phone number or email", placeholder="Phone or email")
            
            b_col1, b_col2 = st.columns([1, 1])
            with b_col1:
                if st.button("Back", use_container_width=True):
                    st.session_state.page_mode = "signin"
                    st.rerun()
            with b_col2:
                if st.button("Submit", use_container_width=True, type="primary"):
                    if recovery_input:
                        st.success("Recovery instructions sent!")
                    else:
                        st.warning("Phone or email luh rawh.")