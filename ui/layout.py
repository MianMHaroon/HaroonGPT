import streamlit as st

def setup_page():
    st.set_page_config(page_title="Haroon GPT", page_icon="🤖", layout="wide")

def inject_custom_css():
    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body, .stApp {
            background: linear-gradient(135deg, rgba(0,0,0,0.6), rgba(0,0,0,0.8)), linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
        }
        #MainMenu, header, footer {visibility: hidden;}
        .main-title {
            text-align: center;
            color: white;
            font-size: 2.5rem;
            font-weight: bold;
            padding-top: 5px;
            margin-bottom: 20px;
            text-shadow: 2px 2px 6px rgba(255,255,255,0.6);
        }
        .block-container {padding-bottom: 120px;}
        .user-message {display: flex; justify-content: flex-end; margin: 12px 0;}
        .user-icon {font-size: 2rem; margin-left: 10px; color: white;}
        .user-content {
            background: rgba(255,255,255,0.18);
            color: white;
            padding: 12px 16px;
            border-radius: 20px 20px 6px 20px;
            max-width: 70%;
            backdrop-filter: blur(5px);
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .bot-message {display: flex; justify-content: flex-start; margin: 12px 0;}
        .bot-icon {font-size: 2rem; margin-right: 10px; color: white;}
        .bot-content {
            background: rgba(255,255,255,0.22);
            color: white;
            padding: 12px 16px;
            border-radius: 20px 20px 20px 6px;
            max-width: 70%;
            backdrop-filter: blur(6px);
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .typing-indicator {
            display: inline-block;
            animation: typing 1.5s infinite;
            font-style: italic;
            font-size: 0.9rem;
        }
        @keyframes typing {0%, 100% {opacity: 0.3;} 50% {opacity: 1;}}
        @keyframes slideInLeft {from {opacity: 0; transform: translateX(-40px);} to {opacity: 1; transform: translateX(0);}}
        @keyframes slideInRight {from {opacity: 0; transform: translateX(40px);} to {opacity: 1; transform: translateX(0);}}
        
        .stChatInput textarea st-emotion-cache-x1bvup exaa2ht1 {
            background: white !important;
            color: black !important;
            border-radius: 5px !important;
        }
        .st-emotion-cache-128upt6, .st-emotion-cache-hzygls {
            padding-bottom: 20px !important;
            background-color: transparent !important;
            box-shadow: none !important;
        }
        .neon-loader {
            margin: 100px auto;
            width: 120px;
            height: 120px;
            border-radius: 50%;
            border: 5px solid rgba(255,255,255,0.2);
            border-top: 5px solid #ffffff;
            animation: glowRotate 1.2s linear infinite;
            box-shadow: 0 0 25px rgba(255,255,255,0.6);
        }
        @keyframes glowRotate {
            0% {transform: rotate(0deg); box-shadow: 0 0 15px white;}
            100% {transform: rotate(360deg); box-shadow: 0 0 25px white;}
        }
        .neon-text {
            text-align: center;
            color: white;
            margin-top: 20px;
            font-size: 1.2rem;
            text-shadow: 0 0 8px rgba(255,255,255,0.7);
        }
    </style>
    """, unsafe_allow_html=True)

def page_title():
    st.markdown('<h1 class="main-title">🤖 Haroon GPT</h1>', unsafe_allow_html=True)
