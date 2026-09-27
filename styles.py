
import streamlit as st

def load_css():
    st.markdown("""
    <style>

    /* =========================
       GLOBAL
    ========================== */

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    html, body, [class*="css"]{
        font-family:'Inter',sans-serif;
    }

    .main{
        padding:1rem 2rem;
        animation:fadeIn .6s ease;
    }

    @keyframes fadeIn{
        from{
            opacity:0;
            transform:translateY(10px);
        }
        to{
            opacity:1;
            transform:none;
        }
    }

    /* =========================
       HERO
    ========================== */

    .hero-title{
        font-size:3.6rem;
        font-weight:900;
        line-height:1.05;
        margin-bottom:6px;

        background:linear-gradient(
            90deg,
            #60A5FA,
            #7C3AED,
            #EC4899
        );

        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
    }

    .hero-subtitle{
        color:#94A3B8;
        font-size:1.05rem;
        margin-bottom:2rem;
    }

    /* =========================
       SIDEBAR
    ========================== */

    section[data-testid="stSidebar"]{

        background:
            linear-gradient(
                180deg,
                #0F172A,
                #1E293B
            );

        border-right:
            1px solid rgba(255,255,255,.08);
    }

    section[data-testid="stSidebar"] *{
        color:white;
    }

    /* =========================
       GLASS CARD
    ========================== */

    .glass-card{

        background:
            rgba(255,255,255,.06);

        backdrop-filter:
            blur(24px);

        border:
            1px solid rgba(255,255,255,.12);

        border-radius:24px;

        padding:1.6rem;

        margin-bottom:1.2rem;

        transition:
            transform .35s ease,
            box-shadow .35s ease,
            border-color .35s ease;

        box-shadow:
            0 10px 35px rgba(0,0,0,.22);
    }

    .glass-card:hover{

        transform:translateY(-5px);

        border-color:#6366F1;

        box-shadow:
            0 18px 45px rgba(99,102,241,.25);
    }

    /* =========================
       UPLOAD CARD
    ========================== */

    .upload-card{

        text-align:center;

        border:
            2px dashed rgba(96,165,250,.35);

        background:
            linear-gradient(
                180deg,
                rgba(37,99,235,.08),
                rgba(124,58,237,.05)
            );
    }

    .upload-card:hover{

        border-color:#60A5FA;

        box-shadow:
            0 0 35px rgba(96,165,250,.25);
    }

    /* =========================
       METRICS
    ========================== */

    div[data-testid="metric-container"]{

        background:#111827;

        border-radius:20px;

        border:1px solid rgba(255,255,255,.08);

        padding:18px;

        transition:.3s;
    }

    div[data-testid="metric-container"]:hover{

        transform:translateY(-3px);

        border-color:#3B82F6;
    }

    /* =========================
       TABS
    ========================== */

    button[data-baseweb="tab"]{

        border-radius:14px;

        padding:12px 22px;

        font-weight:600;

        transition:.25s;
    }

    button[data-baseweb="tab"]:hover{

        background:
            rgba(96,165,250,.12);
    }

    button[data-baseweb="tab"][aria-selected="true"]{

        background:#2563EB !important;

        color:white !important;
    }

    /* =========================
       KEYWORD CHIPS
    ========================== */

    .chip{

        display:inline-block;

        padding:9px 18px;

        margin:6px 8px 6px 0;

        border-radius:999px;

        font-size:.88rem;

        font-weight:600;

        color:white;

        transition:.25s;
    }

    .chip:hover{

        transform:translateY(-2px) scale(1.05);
    }

    .blue{
        background:#2563EB;
    }

    .purple{
        background:#7C3AED;
    }

    .pink{
        background:#EC4899;
    }

    .green{
        background:#10B981;
    }

    .orange{
        background:#F59E0B;
    }

    /* =========================
       PROGRESS BAR
    ========================== */

    div[data-testid="stProgressBar"]>div>div{

        background:
            linear-gradient(
                90deg,
                #60A5FA,
                #7C3AED
            );
    }

    /* =========================
       DOWNLOAD BUTTON
    ========================== */

    .stDownloadButton button{

        width:100%;

        height:3.1rem;

        border-radius:16px;

        background:
            linear-gradient(
                90deg,
                #2563EB,
                #7C3AED
            );

        color:white;

        font-weight:700;

        border:none;

        transition:.25s;
    }

    .stDownloadButton button:hover{

        transform:translateY(-2px);

        box-shadow:
            0 8px 20px rgba(99,102,241,.35);
    }

    /* =========================
       EXPANDERS
    ========================== */

    details{

        border-radius:16px;

        border:
            1px solid rgba(255,255,255,.08);

        overflow:hidden;

        margin-bottom:12px;

        background:
            rgba(255,255,255,.03);
    }

    summary{

        font-weight:600;

        padding:8px;
    }

    /* =========================
       SCROLLBAR
    ========================== */

    ::-webkit-scrollbar{

        width:8px;
    }

    ::-webkit-scrollbar-thumb{

        background:#475569;

        border-radius:10px;
    }

    /* =========================
       MOBILE
    ========================== */

    @media(max-width:768px){

        .hero-title{

            font-size:2.4rem;
        }

        .main{

            padding:1rem;
        }

    }

    </style>
    """, unsafe_allow_html=True)