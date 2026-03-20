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
        @keyframes float { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-10px); } }
        @keyframes glow { 0%,100% { text-shadow:0 0 20px rgba(102,126,234,0.5); } 50% { text-shadow:0 0 40px rgba(102,126,234,0.8), 0 0 80px rgba(245,87,108,0.4); } }
        @keyframes sparkle { 0%,100% { opacity:0.4; } 50% { opacity:1; } }
        @keyframes bgCrossfade {
            0%,6%    { background-image: url('https://images.unsplash.com/photo-1546587348-d12660c30c50?w=1600&q=80'); }
            7%,13%   { background-image: url('https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=1600&q=80'); }
            14%,20%  { background-image: url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1600&q=80'); }
            21%,27%  { background-image: url('https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=1600&q=80'); }
            28%,34%  { background-image: url('https://images.unsplash.com/photo-1529439322271-42931c09bce1?w=1600&q=80'); }
            35%,41%  { background-image: url('https://images.unsplash.com/photo-1444464666168-49d633b86797?w=1600&q=80'); }
            42%,48%  { background-image: url('https://images.unsplash.com/photo-1518709766631-a6a7f45921c3?w=1600&q=80'); }
            49%,55%  { background-image: url('https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=1600&q=80'); }
            56%,62%  { background-image: url('https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=1600&q=80'); }
            63%,69%  { background-image: url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1600&q=80'); }
            70%,76%  { background-image: url('https://images.unsplash.com/photo-1494564605686-2e931f77a8e2?w=1600&q=80'); }
            77%,83%  { background-image: url('https://images.unsplash.com/photo-1491002052546-bf38f186af56?w=1600&q=80'); }
            84%,90%  { background-image: url('https://images.unsplash.com/photo-1457269449834-928af64c684d?w=1600&q=80'); }
            91%,97%  { background-image: url('https://images.unsplash.com/photo-1517299321609-52687d1bc55a?w=1600&q=80'); }
            98%,100% { background-image: url('https://images.unsplash.com/photo-1546587348-d12660c30c50?w=1600&q=80'); }
        }
        .stApp {
            background-size:cover !important; background-position:center !important;
            animation: bgCrossfade 56s ease-in-out infinite;
        }
        .stApp::before {
            content:""; position:fixed; top:0; left:0; width:100%; height:100%;
            background: rgba(0,0,0,0.3);
            z-index:0;
        }
        .stApp > * { position:relative; z-index:1; }
        [data-testid="stSidebar"] { display:none !important; }
        header { display:none !important; }
        .shimmer-title {
            background: linear-gradient(90deg, #ff4d6d, #667eea, #f5576c, #fee140, #ff4d6d);
            background-size: 400% auto;
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            animation: shimmer 4s linear infinite, glow 3s ease-in-out infinite;
        }
        .shimmer-sub {
            background: linear-gradient(90deg, #667eea, #e0e0f0, #f5576c, #667eea);
            background-size: 300% auto;
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            animation: shimmer 6s linear infinite;
        }
        .login-btn button {
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            color: #fff !important; border: none !important;
            font-weight: 700 !important; font-size: 1.05rem !important;
            padding: 12px !important; border-radius: 12px !important; transition: all 0.3s !important;
        }
        .login-btn button:hover { background: linear-gradient(135deg, #764ba2, #f5576c) !important; box-shadow: 0 8px 25px rgba(102,126,234,0.4) !important; }
        .stTextInput input {
            background: rgba(0,0,0,0.4) !important; border: 2px solid rgba(102,126,234,0.5) !important;
            border-radius: 12px !important; color: #fff !important; padding: 12px 16px !important;
            font-size: 1rem !important; text-align: center !important; backdrop-filter: blur(10px) !important;
        }
        .stTextInput input:focus { border-color: #667eea !important; box-shadow: 0 0 20px rgba(102,126,234,0.3) !important; }
        .stTextInput input::placeholder { color: #c0c0e0 !important; }
        @keyframes letterPop { 0% { opacity:0; transform:translateY(20px) scale(0.5); } 100% { opacity:1; transform:translateY(0) scale(1); } }
        @keyframes breathe { 0%,100% { letter-spacing:8px; } 50% { letter-spacing:14px; } }
        .letter { display:inline-block; animation: letterPop 0.6s ease-out both; }
    </style>
    <div style="text-align:center;padding-top:6vh;animation:fadeInUp 1s ease-out;">
        <div style="animation:pulse 2.5s ease-in-out infinite;display:inline-block;font-size:4rem;margin-bottom:5px;">⛪</div>
        <div>
            <svg viewBox="0 0 500 120" style="width:80%;max-width:700px;margin:0 auto;filter:drop-shadow(0 4px 30px rgba(0,0,0,0.8));">
                <defs>
                    <path id="curve" d="M 30,90 Q 250,10 470,90" fill="transparent"/>
                    <linearGradient id="rainbow" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" style="stop-color:#667eea"/>
                        <stop offset="20%" style="stop-color:#f5576c"/>
                        <stop offset="40%" style="stop-color:#00b09b"/>
                        <stop offset="60%" style="stop-color:#fee140"/>
                        <stop offset="80%" style="stop-color:#fa709a"/>
                        <stop offset="100%" style="stop-color:#4facfe"/>
                    </linearGradient>
                </defs>
                <text font-size="58" font-weight="900" fill="url(#rainbow)" font-family="Inter,sans-serif">
                    <textPath href="#curve" startOffset="50%" text-anchor="middle">NACOG 2026</textPath>
                </text>
            </svg>
        </div>
        <div>
            <svg viewBox="0 0 600 70" style="width:75%;max-width:650px;margin:-10px auto 0;filter:drop-shadow(0 2px 15px rgba(0,0,0,0.7));">
                <defs>
                    <path id="curve2" d="M 30,15 Q 300,60 570,15" fill="transparent"/>
                </defs>
                <text font-size="22" font-weight="700" fill="#ffffff" letter-spacing="4" font-family="Inter,sans-serif">
                    <textPath href="#curve2" startOffset="50%" text-anchor="middle">✦ CONFERENCE DASHBOARD ✦</textPath>
                </text>
            </svg>
        </div>
        <div style="display:flex;align-items:center;justify-content:center;gap:12px;margin:10px 0;animation:float 4s ease-in-out infinite;">
            <span style="color:#f5576c;font-size:2rem;animation:sparkle 2s ease-in-out infinite;">✈</span>
            <p style="color:#ffffff;margin:0;font-size:1.3rem;letter-spacing:2px;font-weight:600;
                      text-shadow:0 2px 20px rgba(0,0,0,0.9);">📍 Denver, Colorado &nbsp;•&nbsp; July 2026</p>
            <span style="color:#fee140;font-size:2rem;animation:sparkle 2s ease-in-out 0.5s infinite;">⛰</span>
        </div>
        <p style="color:#e0e0f0;font-size:0.85rem;margin:20px 0 0;letter-spacing:1px;text-shadow:0 2px 10px rgba(0,0,0,0.8);">🔒 AUTHORIZED ACCESS ONLY</p>
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
