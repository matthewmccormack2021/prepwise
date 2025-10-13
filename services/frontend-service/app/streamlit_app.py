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
if "position_name" not in st.session_state:
    st.session_state.position_name = None
if "position_description" not in st.session_state:
    st.session_state.position_description = None
if "show_position_modal" not in st.session_state:
    st.session_state.show_position_modal = True

# ----------------------------
# POSITION SELECTION MODAL
# ----------------------------
def show_position_modal():
    """Display position selection modal"""
    if st.session_state.show_position_modal:
        with st.container():
            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px; margin: 20px 0;">
                <h2 style="color: #1f77b4; margin-bottom: 10px;">🎯 Interview Position Setup</h2>
                <p style="font-size: 16px; color: #666;">Please provide details about the position you'd like to interview for:</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick position selection
            st.markdown("**Quick Select:**")
            quick_positions = ["Software Engineer", "Data Scientist", "Product Manager", "UX Designer", "Marketing Manager", "Sales Representative", "Other"]
            
            col1, col2, col3, col4 = st.columns(4)
            selected_quick = None
            
            # Default descriptions for quick select
            default_descriptions = {
                "Software Engineer": "Full-stack development role focusing on building scalable web applications, working with modern technologies, and collaborating with cross-functional teams.",
                "Data Scientist": "Role involving data analysis, machine learning model development, statistical analysis, and deriving actionable insights from large datasets.",
                "Product Manager": "Strategic role responsible for product vision, roadmap planning, stakeholder management, and driving product development from conception to launch.",
                "UX Designer": "User experience design role focusing on creating intuitive and engaging user interfaces, conducting user research, and improving product usability."
            }
            
            with col1:
                if st.button("👨‍💻 Software Engineer", use_container_width=True):
                    selected_quick = "Software Engineer"
                    st.session_state.position_description = default_descriptions["Software Engineer"]
            with col2:
                if st.button("📊 Data Scientist", use_container_width=True):
                    selected_quick = "Data Scientist"
                    st.session_state.position_description = default_descriptions["Data Scientist"]
            with col3:
                if st.button("📋 Product Manager", use_container_width=True):
                    selected_quick = "Product Manager"
                    st.session_state.position_description = default_descriptions["Product Manager"]
            with col4:
                if st.button("🎨 UX Designer", use_container_width=True):
                    selected_quick = "UX Designer"
                    st.session_state.position_description = default_descriptions["UX Designer"]
            
            if selected_quick:
                st.session_state.position_name = selected_quick
            
            position_name = st.text_input(
                "Position Name",
                value=st.session_state.position_name or "",
                placeholder="e.g., Software Engineer, Data Scientist, Product Manager",
                help="Enter the job title you're preparing for"
            )
            
            position_description = st.text_area(
                "Position Description",
                value=st.session_state.position_description or "",
                placeholder="Describe the role, key responsibilities, required skills, or any specific details about the position...",
                height=150,
                help="Provide details about the role to help customize your interview experience"
            )
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col2:
                if st.button("Start Interview", type="primary", use_container_width=True):
                    if position_name.strip():
                        st.session_state.position_name = position_name.strip()
                        st.session_state.position_description = position_description.strip()
                        st.session_state.show_position_modal = False
                        
                        # Add welcome message to start the interview
                        welcome_message = f"Hello! I'm your AI interviewer for the {position_name} position. I'm here to help you practice and prepare for your interview. Let's start with an introduction - could you tell me a bit about yourself and why you're interested in this role?"
                        st.session_state.messages.append({"role": "assistant", "content": welcome_message})
                        
                        st.success(f"🎉 Interview setup complete! Position: {position_name}")
                        st.rerun()
                    else:
                        st.error("Please enter a position name to continue.")
            
            st.markdown("---")
            return False  # Modal is still open
    return True  # Modal is closed

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
                # Build conversation context with position information
                position_context = ""
                if st.session_state.position_name:
                    position_context = f"Interview Position: {st.session_state.position_name}"
                    if st.session_state.position_description:
                        position_context += f"\nPosition Description: {st.session_state.position_description}"
                    position_context += "\n\n"
                
                context = ""
                for msg in st.session_state.messages[:-1]:
                    role = "Interviewer" if msg["role"] == "assistant" else "Candidate"
                    context += f"{role}: {msg['content']}\n"

                contextual_query = (
                    f"{position_context}Previous conversation:\n{context}\n\nCurrent question: {message_text}"
                    if context
                    else f"{position_context}{message_text}"
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
# SIDEBAR – POSITION INFO & MICROPHONE CONTROL
# ----------------------------
if st.session_state.position_name:
    st.sidebar.header("🎯 Current Position")
    st.sidebar.info(f"**{st.session_state.position_name}**")
    if st.session_state.position_description:
        with st.sidebar.expander("Position Details"):
            st.text(st.session_state.position_description[:200] + "..." if len(st.session_state.position_description) > 200 else st.session_state.position_description)
    
    if st.sidebar.button("🔄 Change Position"):
        st.session_state.show_position_modal = True
        st.rerun()
    
    st.sidebar.markdown("---")

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

# Show position modal if needed
if not show_position_modal():
    st.stop()  # Stop execution until position is set

st.subheader("💬 Practice and Feel the Real Interview Experience")

# Display conversation
for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(msg["content"])

# Handle pending messages
if st.session_state.pending_message:
    # Display the pending user message immediately
    with st.chat_message("user"):
        st.markdown(st.session_state.pending_message)
    
    # Process with AI (this will add the user message to chat history)
    send_to_llm(st.session_state.pending_message)
    st.session_state.pending_message = None

# Text chat input
user_input = st.chat_input("Type your answer or follow-up question here...")

if user_input:
    send_to_llm(user_input)
