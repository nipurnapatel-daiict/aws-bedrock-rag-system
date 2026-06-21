import sys
import os
import requests
import streamlit as st
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.core.constants import ApplicationConstants

API_BASE_URL = "http://127.0.0.1:8000"
FULL_API_URL = f"{API_BASE_URL.rstrip('/')}/{ApplicationConstants.API_PREFIX.lstrip('/')}"

st.set_page_config(page_title="RAG Chat", layout="wide")

## session state
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploader_version" not in st.session_state:
    st.session_state.uploader_version = 0
if "processing" not in st.session_state:
    st.session_state.processing = False

# New API Management Functions 
def delete_thread(thread_id):
    try:
        response = requests.delete(f"{FULL_API_URL}/threads/{thread_id}")
        return response.status_code == 200
    except:
        return False

def rename_thread(thread_id, new_title):
    try:
        response = requests.patch(f"{FULL_API_URL}/threads/{thread_id}", json={"title": new_title})
        return response.status_code == 200
    except:
        return False

#API Functions
def fetch_threads():
    try:
        response = requests.get(f"{FULL_API_URL}/threads")
        if response.status_code == 200:
            return response.json().get("threads", [])
    except:
        return []
    return []

def fetch_messages(thread_id):
    try:
        response = requests.get(f"{FULL_API_URL}/messages/{thread_id}")
        if response.status_code == 200:
            res_json = response.json()
            return res_json.get("messages", res_json.get("data", []))
    except:
        return []
    return []

def upload_file(file):
    try:
        files = {"file": (file.name, file, file.type)}
        response = requests.post(f"{FULL_API_URL}/upload", files=files)
        return response.status_code == 200
    except:
        return False

def ask_question(query):
    payload = {"query": query, "thread_id": st.session_state.thread_id}
    try:
        response = requests.post(f"{FULL_API_URL}/ask", json=payload)
        if response.status_code == 200:
            data = response.json()
            if "response" in data:
                return {"response": data.get("response"), "thread_id": data.get("thread_id")}
            return data.get("data")
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Exception in ask_question: {str(e)}")
        return None
    
def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.05)

# SIDEBAR 
with st.sidebar:
    st.title("⚙️ Management")
    with st.expander("📤 Upload New Document", expanded=False):
        uploaded_file = st.file_uploader(
            "Drop PDF/TXT here", 
            type=["pdf", "txt"], 
            label_visibility="collapsed",
            key=f"file_up_{st.session_state.uploader_version}"
        )
        
        if uploaded_file:
            if st.button("Upload Document", use_container_width=True, type="primary"):
                with st.spinner("Uploading..."):
                    if upload_file(uploaded_file):
                        st.success("Success!")
                        st.session_state.uploader_version += 1
                        st.rerun()

    st.divider()
    st.title("💬 Chat History")
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.thread_id = None
        st.session_state.messages = []
        st.rerun()

    threads = fetch_threads()
    for t in threads:
        t_id = t.get("thread_id")
        t_title = t.get("title", "Untitled Chat")
        if st.button(f"{t_title}", key=f"btn_{t_id}", use_container_width=True):
            st.session_state.thread_id = t_id
            st.session_state.messages = fetch_messages(t_id)
            st.rerun()
            

# MAIN UI 
st.title("RAG Application")

if st.session_state.thread_id:
    st.caption(f"Session: {st.session_state.thread_id}")

# RENDER HISTORY
chat_container = st.container()
with chat_container:
    for m in st.session_state.messages:
        msg = m.get("_source", m) 
        role = msg.get("role", ApplicationConstants.CHATBOT_ROLE)
        # Map backend roles to Streamlit chat_message roles
        display_role = "assistant" if role == ApplicationConstants.CHATBOT_ROLE else role
        content = msg.get("content", "")
        with st.chat_message(display_role):
            st.markdown(content)

# CHAT INPUT
if prompt := st.chat_input("Ask a question...", disabled=st.session_state.processing):
    # Add User message to state
    st.session_state.messages.append({"role": ApplicationConstants.USER_ROLE, "content": prompt})
    st.session_state.processing = True
    st.rerun()

if st.session_state.processing and len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == ApplicationConstants.USER_ROLE:
    last_user_msg = st.session_state.messages[-1]["content"]
    
    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Generating answer..."):
            result = ask_question(last_user_msg)
            if result:
                answer = result.get("response")
                st.session_state.thread_id = result.get("thread_id")
                
                st.write_stream(stream_data(answer))
                
                st.session_state.messages.append({"role": ApplicationConstants.CHATBOT_ROLE, "content": answer})
            else:
                msg = "Failed to get a response from the server. Check backend logs."
                st.error(msg)
                st.session_state.messages.append({"role": ApplicationConstants.CHATBOT_ROLE, "content": msg})
    
    st.session_state.processing = False
    st.rerun()
