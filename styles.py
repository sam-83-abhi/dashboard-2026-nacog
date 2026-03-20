import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
        .block-container { padding-top: 1.5rem; }

        /* Dark theme - nuclear white override */
        .stApp { background-color: #0a0a1a; color: #ffffff !important; }
        .stApp *, .stMarkdown *, [data-testid="stMarkdownContainer"] *,
        [data-testid="stMetricValue"], [data-testid="stMetricLabel"],
        [data-testid="stMetricDelta"], [data-testid="stTable"] *,
        .stAlert *, .stDataFrame *, [data-testid="stDataFrame"] *,
        .stSelectbox label, .stMultiSelect label,
        .stFileUploader label, .stTextInput label,
        [data-testid="stWidgetLabel"] *, [data-testid="stText"],
        [data-testid="column"] *, [data-testid="stVerticalBlock"] *,
        h1, h2, h3, h4, h5, h6, p, span, label, div, li, td, th, caption,
        strong, em, b, i, a { color: #ffffff !important; }

        .stTextInput input, .stTextArea textarea {
            color: #ffffff !important; background: #1a1a3a !important;
            border: 1px solid #667eea !important; caret-color: #ffffff !important;
        }
        .stTextInput input::placeholder { color: #a0a0c0 !important; }

        [data-testid="stDataFrame"] * { color: #ffffff !important; }
        [data-testid="stDataFrame"] input { color: #ffffff !important; background: #1a1a3a !important; border: 1px solid #667eea !important; }
        [data-testid="stDataFrame"] button { color: #ffffff !important; }
        [data-testid="stDataFrame"] svg { fill: #ffffff !important; }
        .stDataFrame th, .stDataFrame td { color: #ffffff !important; background: #12122a !important; }
        [data-testid="stDataFrame"] input::placeholder { color: #a0a0c0 !important; }

        .metric-card { padding:22px 18px; border-radius:16px; color:white; text-align:center; box-shadow:0 8px 32px rgba(0,0,0,0.3); }
        .metric-card h2 { font-size:2.4rem; margin:0; font-weight:700; color:#fff !important; }
        .metric-card p { font-size:0.85rem; margin:5px 0 0; opacity:0.9; text-transform:uppercase; letter-spacing:1px; color:#fff !important; }
        .mc-purple { background: linear-gradient(135deg, #667eea, #764ba2); }
        .mc-green  { background: linear-gradient(135deg, #00b09b, #96c93d); }
        .mc-blue   { background: linear-gradient(135deg, #4facfe, #00f2fe); }
        .mc-orange { background: linear-gradient(135deg, #f093fb, #f5576c); }
        .mc-pink   { background: linear-gradient(135deg, #fa709a, #fee140); }

        /* Sidebar */
        div[data-testid="stSidebar"], div[data-testid="stSidebar"] > div,
        section[data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
            background: #0a0a1a !important; border-right: 1px solid #1a1a3a;
        }
        div[data-testid="stSidebar"] *, section[data-testid="stSidebar"] *,
        [data-testid="stSidebar"] label, [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] div,
        [data-testid="stSidebar"] small, [data-testid="stSidebar"] button span,
        [data-testid="stSidebar"] [data-baseweb] *, [data-testid="stSidebar"] [role="button"],
        [data-testid="stSidebar"] svg { color: #ffffff !important; fill: #ffffff !important; }
        [data-testid="stSidebar"] button {
            background:#667eea !important; color:#ffffff !important;
            border:2px solid #764ba2 !important; font-weight:700 !important; font-size:1rem !important; padding:10px !important;
        }
        [data-testid="stSidebar"] button:hover { background:#764ba2 !important; }
        [data-testid="stSidebar"] button span { color:#ffffff !important; }
        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
            background:rgba(102,126,234,0.2) !important; border:2px dashed #667eea !important;
        }
        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] * { color:#ffffff !important; }
        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button { background:#f5576c !important; border:none !important; }
        [data-testid="stSidebar"] h5 { color:#ffffff !important; font-size:1.1rem !important; }
        [data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] { background:#667eea !important; }
        [data-testid="stSidebar"] [data-baseweb="select"] * { color:#ffffff !important; }

        /* Dropdown menu styling */
        [data-baseweb="popover"], [data-baseweb="menu"] { background:#1a1a3a !important; border:1px solid #667eea !important; }
        [data-baseweb="popover"] li, [data-baseweb="menu"] li { color:#ffffff !important; }
        [data-baseweb="popover"] li:hover, [data-baseweb="menu"] li:hover { background:#667eea !important; }
        [data-baseweb="popover"] li[aria-selected="true"], [data-baseweb="menu"] li[aria-selected="true"] { background:#764ba2 !important; }
        [data-baseweb="select"] [data-baseweb="tag"] { background:#667eea !important; color:#ffffff !important; }
        [data-baseweb="input"] { background:#1a1a3a !important; color:#ffffff !important; }

        .section-divider { height:3px; border-radius:2px; margin:10px 0 20px; background:linear-gradient(90deg,#667eea,#764ba2,#f5576c,#fee140); }

        .reg-table { width:100%; border-collapse:collapse; font-size:0.85rem; }
        .reg-table th { background:#667eea; color:#fff; padding:10px 12px; text-align:left; font-weight:600; position:sticky; top:0; }
        .reg-table td { padding:8px 12px; color:#ffffff; border-bottom:1px solid #1a1a3a; }
        .reg-table tr:hover td { background:rgba(102,126,234,0.15); }
        .reg-table tr:nth-child(even) td { background:rgba(255,255,255,0.03); }
    </style>
    """, unsafe_allow_html=True)
