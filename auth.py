import streamlit as st

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if st.session_state.authenticated:
        return True
    st.markdown("""
    <style>
        @keyframes fadeInUp { from { opacity:0; transform:translateY(30px); } to { opacity:1; transform:translateY(0); } }
        @keyframes pulse { 0%,100% { transform:scale(1); } 50% { transform:scale(1.05); } }
        @keyframes bgSlide {
            0%   { background-image: url('https://images.pexels.com/photos/417074/pexels-photo-417074.jpeg?auto=compress&w=1400'); }
            20%  { background-image: url('https://images.pexels.com/photos/417074/pexels-photo-417074.jpeg?auto=compress&w=1400'); }
            25%  { background-image: url('https://images.pexels.com/photos/1632790/pexels-photo-1632790.jpeg?auto=compress&w=1400'); }
            45%  { background-image: url('https://images.pexels.com/photos/1632790/pexels-photo-1632790.jpeg?auto=compress&w=1400'); }
            50%  { background-image: url('https://images.pexels.com/photos/1054218/pexels-photo-1054218.jpeg?auto=compress&w=1400'); }
            70%  { background-image: url('https://images.pexels.com/photos/1054218/pexels-photo-1054218.jpeg?auto=compress&w=1400'); }
            75%  { background-image: url('https://images.pexels.com/photos/1578750/pexels-photo-1578750.jpeg?auto=compress&w=1400'); }
            95%  { background-image: url('https://images.pexels.com/photos/1578750/pexels-photo-1578750.jpeg?auto=compress&w=1400'); }
            100% { background-image: url('https://images.pexels.com/photos/417074/pexels-photo-417074.jpeg?auto=compress&w=1400'); }
        }
        .stApp { background-size:cover !important; background-position:center !important; animation:bgSlide 32s infinite; }
        .stApp::before { content:""; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(10,10,30,0.55); z-index:0; }
        .stApp > * { position:relative; z-index:1; }
        .login-card { animation:fadeInUp 0.8s ease-out; }
        .login-card:hover { transform:translateY(-5px); box-shadow:0 30px 80px rgba(0,0,0,0.5) !important; transition:all 0.3s; }
        .login-emoji { animation:pulse 2s ease-in-out infinite; display:inline-block; }
    </style>
    <div style="display:flex;justify-content:center;align-items:center;min-height:70vh;">
        <div class="login-card" style="background:rgba(26,26,46,0.55);backdrop-filter:blur(8px);padding:0;border-radius:20px;
                    text-align:center;box-shadow:0 20px 60px rgba(0,0,0,0.4);max-width:420px;width:100%;overflow:hidden;">
            <div style="padding:35px 40px 30px;">
                <div class="login-emoji" style="font-size:3rem;margin-bottom:8px;">🎉</div>
                <h1 style="color:#ff4d6d;margin:0 0 5px;font-size:2rem;font-weight:700;">NACOG 2026</h1>
                <p style="color:#e0e0f0;margin:0 0 5px;font-size:1.1rem;font-weight:600;">Conference Dashboard</p>
                <p style="color:#c0c0d0;margin:0 0 20px;font-size:0.9rem;">📍 Denver, Colorado</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        pwd = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Enter password")
        if st.button("🔓 Login", use_container_width=True):
            if pwd == st.secrets.get("password", "nacog2026"):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Incorrect password")
    return False
