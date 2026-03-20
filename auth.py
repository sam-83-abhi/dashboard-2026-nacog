import streamlit as st

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if st.session_state.authenticated:
        return True
    st.markdown("""
    <style>
        @keyframes fadeInUp { from { opacity:0; transform:translateY(40px); } to { opacity:1; transform:translateY(0); } }
        @keyframes pulse { 0%,100% { transform:scale(1); } 50% { transform:scale(1.08); } }
        @keyframes shimmer { 0% { background-position:200% center; } 100% { background-position:-200% center; } }
        @keyframes bgCrossfade {
            0%,18%   { opacity:1; background-image: url('https://images.unsplash.com/photo-1546587348-d12660c30c50?w=1600&q=80'); }
            22%,43%  { opacity:1; background-image: url('https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=1600&q=80'); }
            47%,68%  { opacity:1; background-image: url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1600&q=80'); }
            72%,93%  { opacity:1; background-image: url('https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=1600&q=80'); }
            97%,100% { opacity:1; background-image: url('https://images.unsplash.com/photo-1546587348-d12660c30c50?w=1600&q=80'); }
        }
        .stApp {
            background-size:cover !important; background-position:center !important;
            animation: bgCrossfade 28s ease-in-out infinite;
        }
        .stApp::before {
            content:""; position:fixed; top:0; left:0; width:100%; height:100%;
            background: linear-gradient(135deg, rgba(10,10,30,0.7), rgba(48,43,99,0.5), rgba(10,10,30,0.7));
            z-index:0;
        }
        .stApp > * { position:relative; z-index:1; }
        [data-testid="stSidebar"] { display:none !important; }
        header { display:none !important; }

        .login-card {
            animation: fadeInUp 1s ease-out;
            transition: all 0.4s ease;
        }
        .login-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 35px 90px rgba(102,126,234,0.3) !important;
        }
        .login-emoji { animation: pulse 2.5s ease-in-out infinite; display:inline-block; }
        .shimmer-text {
            background: linear-gradient(90deg, #ff4d6d, #667eea, #f5576c, #fee140, #ff4d6d);
            background-size: 400% auto;
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            animation: shimmer 4s linear infinite;
        }
        .login-divider {
            height:3px; border-radius:2px; margin:0;
            background: linear-gradient(90deg, transparent, #667eea, #f5576c, #fee140, transparent);
        }
        .login-btn button {
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            color: #fff !important; border: none !important;
            font-weight: 700 !important; font-size: 1.05rem !important;
            padding: 12px !important; border-radius: 12px !important;
            transition: all 0.3s !important;
        }
        .login-btn button:hover {
            background: linear-gradient(135deg, #764ba2, #f5576c) !important;
            box-shadow: 0 8px 25px rgba(102,126,234,0.4) !important;
        }
        .stTextInput input {
            background: rgba(255,255,255,0.08) !important;
            border: 2px solid rgba(102,126,234,0.4) !important;
            border-radius: 12px !important; color: #fff !important;
            padding: 12px 16px !important; font-size: 1rem !important;
            text-align: center !important;
        }
        .stTextInput input:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 20px rgba(102,126,234,0.3) !important;
        }
        .stTextInput input::placeholder { color: #a0a0c0 !important; }
    </style>
    <div style="display:flex;justify-content:center;align-items:center;min-height:75vh;">
        <div class="login-card" style="background:rgba(20,20,50,0.6);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
                    padding:0;border-radius:24px;text-align:center;
                    box-shadow:0 25px 70px rgba(0,0,0,0.5);max-width:440px;width:100%;
                    border:1px solid rgba(102,126,234,0.2);overflow:hidden;">
            <div style="padding:40px 45px 10px;">
                <div class="login-emoji" style="font-size:3.5rem;margin-bottom:12px;">🎉</div>
                <h1 class="shimmer-text" style="margin:0 0 6px;font-size:2.2rem;font-weight:800;">NACOG 2026</h1>
                <p style="color:#e0e0f0;margin:0 0 4px;font-size:1.15rem;font-weight:600;letter-spacing:1px;">Conference Dashboard</p>
                <p style="color:#a0a0c0;margin:0 0 5px;font-size:0.9rem;">📍 Denver, Colorado &nbsp;•&nbsp; July 2026</p>
            </div>
            <div class="login-divider"></div>
            <div style="padding:15px 45px 30px;">
                <p style="color:#c0c0e0;font-size:0.8rem;margin:0 0 8px;letter-spacing:0.5px;">🔒 AUTHORIZED ACCESS ONLY</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1.2, 1, 1.2])
    with col2:
        pwd = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="🔑  Enter password")
        st.markdown('<div class="login-btn">', unsafe_allow_html=True)
        if st.button("🔓 Login", use_container_width=True):
            if pwd == st.secrets.get("password", "nacog2026"):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Incorrect password")
        st.markdown('</div>', unsafe_allow_html=True)
    return False
