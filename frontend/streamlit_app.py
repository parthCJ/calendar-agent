# frontend/streamlit_app.py

import streamlit as st
import requests
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Personal Agent Appointment Booker",
    page_icon="💬",
    layout="centered"
)

st.title("💬 TailorTalk Appointment Booker")
st.caption("Your personal AI assistant for booking appointments on Google Calendar.")

# --- API CONFIGURATION ---
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
CHAT_ENDPOINT = f"{BACKEND_URL}/chat"

# --- SESSION STATE INITIALIZATION ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you book an appointment today?"}]

# --- CHAT INTERFACE ---

# Display chat messages from history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Accept user input
if prompt := st.chat_input("What would you like to do?"):
    # Add user message to session state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare request for the backend
    payload = {
        "session_id": st.session_state.session_id,
        "message": prompt
    }

    # Display a spinner while waiting for the backend response
    with st.spinner("Thinking..."):
        try:
            response = requests.post(CHAT_ENDPOINT, json=payload)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            bot_response = response.json()
            
            # Add assistant response to session state and display it
            st.session_state.messages.append({"role": "assistant", "content": bot_response["response"]})
            with st.chat_message("assistant"):
                st.markdown(bot_response["response"])

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to the backend: {e}")
            st.session_state.messages.append({"role": "assistant", "content": f"Sorry, I'm having trouble connecting to my brain. Please try again later. Error: {e}"})
            with st.chat_message("assistant"):
                 st.markdown(f"Sorry, I'm having trouble connecting to my brain. Please try again later. Error: {e}")