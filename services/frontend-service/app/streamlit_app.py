import streamlit as st
import requests
from streamlit_mic_recorder import mic_recorder
import io

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

# ----------------------------
# STATE INITIALIZATION
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = None
if "audio_recording" not in st.session_state:
    st.session_state.audio_recording = None
if "pending_message" not in st.session_state:
    st.session_state.pending_message = None
if "processing_message" not in st.session_state:
    st.session_state.processing_message = False

# ----------------------------
# HELPER FUNCTIONS
# ----------------------------
def transcribe_audio(audio_bytes: bytes):
    """Send recorded audio bytes to transcription API and return text"""
    try:
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "audio.webm"
        files = {"audio_file": ("audio.webm", audio_file, "audio/webm")}
        res = requests.post(TRANSCRIBE_API_URL, files=files, timeout=300)

        if res.status_code == 200:
            transcription = res.text.strip()
            return transcription if transcription else None
        else:
            return None
    except Exception as e:
        return None


def send_to_llm(message_text: str):
    """Send a message or transcription to the LLM backend"""
    if not message_text or st.session_state.processing_message:
        return

    # Set processing flag to prevent duplicates
    st.session_state.processing_message = True
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": message_text})
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Build conversation context
                context = ""
                for msg in st.session_state.messages[:-1]:
                    role = "Interviewer" if msg["role"] == "assistant" else "Candidate"
                    context += f"{role}: {msg['content']}\n"

                contextual_query = (
                    f"Previous conversation:\n{context}\n\nCurrent question: {message_text}"
                    if context
                    else message_text
                )

                payload = {"query": contextual_query}
                res = requests.post(LLM_API_URL, json=payload, timeout=120)

                if res.status_code == 200:
                    data = res.json()
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
    
    # Reset processing flag
    st.session_state.processing_message = False

# ----------------------------
# SIDEBAR – MICROPHONE CONTROL
# ----------------------------
st.sidebar.header("🎙️ Record Your Answer")

audio_data = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹️ Stop Recording",
    just_once=False,
    key="recorder",
)

if audio_data and audio_data.get("bytes"):
    st.session_state.audio_recording = audio_data["bytes"]
    st.sidebar.audio(audio_data["bytes"], format="audio/webm")

    if st.sidebar.button("Transcribe Recording"):
        with st.spinner("Transcribing..."):
            transcription = transcribe_audio(audio_data["bytes"])
            if transcription:
                st.session_state.transcribed_text = transcription
                st.sidebar.success("✅ Transcription complete!")
            else:
                st.sidebar.error("❌ Transcription failed. Please try again.")

# Show transcribed text if available
if st.session_state.transcribed_text:
    st.sidebar.text_area(
        "Transcribed Text", st.session_state.transcribed_text, height=150
    )
    if st.sidebar.button("Send Transcription to Chat"):
        st.session_state.pending_message = st.session_state.transcribed_text
        st.session_state.transcribed_text = None  # clear after sending
        st.rerun()

# ----------------------------
# MAIN CHAT INTERFACE
# ----------------------------
st.subheader("💬 Practice and Feel the Real Interview Experience")

# Display conversation
for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(msg["content"])

# Handle pending messages
if st.session_state.pending_message:
    send_to_llm(st.session_state.pending_message)
    st.session_state.pending_message = None

# Text chat input
user_input = st.chat_input("Type your answer or follow-up question here...")

if user_input:
    send_to_llm(user_input)
