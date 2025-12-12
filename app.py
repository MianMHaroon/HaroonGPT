import streamlit as st
from ui.layout import setup_page, inject_custom_css, page_title
from ui.components import (
    render_user_message, render_bot_message,
    render_typing_effect, show_loader, show_thinking
)

# 1️⃣ Setup UI
setup_page()
inject_custom_css()
page_title()

if "qa_pipeline" not in st.session_state:
    loader = show_loader() 

from config import Config
from core.pipeline_loader import init_pipeline


# 3️⃣ Pipeline init
if "qa_pipeline" not in st.session_state:
    st.session_state["qa_pipeline"] = init_pipeline(Config)
    loader.empty()

# 4️⃣ Session State
if "messages" not in st.session_state:
    st.session_state["messages"] = [{
        "role": "bot",
        "content": (
            "Hello! 👋\n\n"
            "Welcome to **HaroonGPT**, a personal AI assistant created by **Muhammad Haroon**.\n"
            "I'm here to assist you with inquiries about Haroon and his work."
        )
    }]

if "bot_typing" not in st.session_state:
    st.session_state["bot_typing"] = False

if "last_bot_index" not in st.session_state:
    st.session_state["last_bot_index"] = -1

# 5️⃣ Render messages
for i, msg in enumerate(st.session_state["messages"]):
    if msg["role"] == "user":
        render_user_message(msg["content"])
    else:
        if i <= st.session_state["last_bot_index"]:
            render_bot_message(msg["content"])
        else:
            placeholder = st.empty()
            render_typing_effect(msg["content"], placeholder)
            st.session_state["last_bot_index"] = i

if st.session_state["bot_typing"]:
    show_thinking()

# 6️⃣ Chat input
user_input = st.chat_input("Type your message...", disabled=st.session_state["bot_typing"])

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.session_state["bot_typing"] = True
    st.rerun()

# 7️⃣ Answer
if st.session_state.get("bot_typing"):
    qa = st.session_state["qa_pipeline"]
    result = qa.answer(
        st.session_state["messages"][-1]["content"],
        st.session_state["messages"][:-1]
    )
    reply = result if isinstance(result, str) else result.get("answer", str(result))

    st.session_state["messages"].append({"role": "bot", "content": reply})
    st.session_state["bot_typing"] = False
    st.rerun()
