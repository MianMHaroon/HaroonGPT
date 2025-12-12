import streamlit as st
import time

def render_user_message(content):
    st.markdown(f"""
    <div class="user-message">
        <div class="user-content">{content}</div>
        <i class="fa-solid fa-user user-icon"></i>
    </div>
    """, unsafe_allow_html=True)

def render_bot_message(content):
    st.markdown(f"""
    <div class="bot-message">
        <span class="bot-icon">🤖</span>
        <div class="bot-content">{content}</div>
    </div>
    """, unsafe_allow_html=True)

def render_typing_effect(full_text, placeholder):
    displayed = ""
    for ch in full_text:
        displayed += ch
        placeholder.markdown(f"""
            <div class="bot-message">
                <span class="bot-icon">🤖</span>
                <div class="bot-content">{displayed}</div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(0.015)

def show_loader():
    loader = st.empty()
    loader.markdown("""
        <div class="neon-loader"></div>
        <div class="neon-text">Loading pipeline...</div>
    """, unsafe_allow_html=True)
    return loader

def show_thinking():
    st.markdown("""
        <div class="bot-message">
            <span class="bot-icon">🤖</span>
            <div class="bot-content"><span class="typing-indicator">Thinking...</span></div>
        </div>
    """, unsafe_allow_html=True)
