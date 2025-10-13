import streamlit as st
import requests

st.set_page_config(page_title="Chat + Transcribe", page_icon="🎧", layout="centered")

# ----------------------------
# CONFIGURATION
# ----------------------------
TRANSCRIBE_API_URL = "http://transcription-service:9000/asr"
LLM_API_URL = "http://backend-service:8002/chat"

# ----------------------------
# APP TITLE
# ----------------------------
st.title("PrepWise AI Interview Practice Platform")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------
# SIDEBAR – AUDIO TRANSCRIPTION
# ----------------------------
# st.sidebar.header("🎙️ Audio Transcription")

# uploaded_audio = st.sidebar.file_uploader("Upload audio", type=["mp3", "wav", "m4a", "ogg"])

# if uploaded_audio is not None:
#     try:
#         files = {"file": (uploaded_audio.name, uploaded_audio, uploaded_audio.type)}
#         res = requests.post(TRANSCRIBE_API_URL, files=files, timeout=300)

#         if res.status_code == 200:
#             transcription = res.json().get("text", "").strip()
#             if transcription:
#                 st.sidebar.success("✅ Transcription complete!")
#                 st.sidebar.text_area("Result:", transcription, height=150)
#                 if st.sidebar.button("Send to Chat"):
#                     st.session_state.messages.append({"role": "user", "content": transcription})
#             else:
#                 st.sidebar.warning("No text returned from transcription.")
#         else:
#             st.sidebar.error(f"❌ Transcription failed: {res.status_code}\n{res.text}")
#     except Exception as e:
#         st.sidebar.error(f"Connection error: {e}")

# ----------------------------
# MAIN CHAT INTERFACE
# ----------------------------
st.subheader("💬 Practice and feel the real interview experience")

# Display chat history
for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Build conversation context for the LLM
                conversation_context = ""
                for msg in st.session_state.messages[:-1]:  # All messages except the current one
                    role = "Interviewer" if msg["role"] == "assistant" else "Candidate"
                    conversation_context += f"{role}: {msg['content']}\n"
                
                # Add the current user input with context
                if conversation_context:
                    contextual_query = f"Previous conversation:\n{conversation_context}\n\nCurrent question: {user_input}"
                else:
                    contextual_query = user_input
                
                payload = {"query": contextual_query}
                res = requests.post(LLM_API_URL, json=payload, timeout=120)

                if res.status_code == 200:
                    data = res.json()
                    print(data)
                    # Parse the backend response format
                    if data.get("status") == "success":
                        reply = data.get("response", "No response received")
                    else:
                        reply = f"Error: {data.get('error', 'Unknown error')}"
                else:
                    reply = f"Error {res.status_code}: {res.text}"
            except Exception as e:
                reply = f"Connection error: {e}"

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
