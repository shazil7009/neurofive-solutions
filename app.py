import os
from dotenv import load_dotenv
from groq import Groq
import streamlit as st

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="Neurofive AI Assistant", page_icon="🤖", layout="wide"
)

# Custom CSS for Dark Theme adjustments & Dark Chat Input with White Text
st.markdown(
    """
    <style>
        /* Chat Input Container Dark with White Border */
        div[data-testid="stChatInput"] {
            background-color: #1b222c !important;
            border: 1px solid #ffffff !important;
            border-radius: 12px !important;
            padding: 4px !important;
        }
        /* Text inside Chat Input White */
        div[data-testid="stChatInput"] textarea {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        /* Placeholder text color */
        div[data-testid="stChatInput"] textarea::placeholder {
            color: #aaaaaa !important;
            -webkit-text-fill-color: #aaaaaa !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize Groq Client
api_key = os.getenv("GROQ_API_KEY")
client = None
if api_key:
    try:
        client = Groq(api_key=api_key)
    except Exception:
        pass

# Sidebar UI with Green Branding
with st.sidebar:
    st.markdown(
        """
        <div style='display: flex; align-items: center; margin-bottom: 5px;'>
            <span style='font-size: 32px; font-weight: 900; color: #00e676; margin-right: 8px; font-family: sans-serif;'>N5</span>
            <div>
                <div style='font-size: 16px; font-weight: bold; color: #ffffff; line-height: 1.1;'>Neurofive</div>
                <div style='font-size: 14px; font-weight: bold; color: #00e676; line-height: 1.1;'>Solutions</div>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown("#### 🤖 AI Support Assistant")
    st.markdown("---")
    st.markdown("**Powered by:**")
    st.markdown("- Groq API\n- Llama LLM\n- Python\n- Streamlit")
    st.markdown("---")
    st.markdown("**Try asking:**")

    sample_queries = [
        "What is Python used for?",
        "How does Llama LLM work?",
        "What is cloud computing?",
    ]

    selected_sample = None
    for query in sample_queries:
        if st.button(query, use_container_width=True):
            selected_sample = query

# Main Chat Interface Header
st.markdown(
    """
    <div style='background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%); padding: 30px; border-radius: 12px; color: white; text-align: center; margin-bottom: 25px;'>
        <h1 style='margin:0; font-size: 2.5rem;'>🤖 Neurofive AI Assistant</h1>
        <p style='margin:5px 0 0 0; font-size: 1.1rem; opacity: 0.9;'>Your intelligent AI partner for technology, software and AI solutions</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Prior Chat Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Ask Neurofive AI anything...")

if selected_sample:
    user_prompt = selected_sample

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if not client:
                bot_reply = "⚠️ API Key missing! Please set your GROQ_API_KEY in the .env file."
                st.error(bot_reply)
            else:
                try:
                    system_message = (
                        "You are Neurofive AI Assistant, a professional, helpful, and intelligent AI expert "
                        "representing Neurofive Solutions. Provide clear, well-structured, and accurate technical and business answers."
                    )
                    
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": user_prompt}
                        ]
                    )
                    bot_reply = response.choices[0].message.content
                    st.markdown(bot_reply)
                except Exception as e:
                    error_str = str(e)
                    if "429" in error_str or "rate_limit" in error_str.lower():
                        bot_reply = (
                            "⚠️ **API Quota Limit Reached (Error 429):** Groq API ki limit exceed ho gayi hai. "
                            "Baraye meharbani apni Groq console se nayi key generate karein."
                        )
                    else:
                        bot_reply = f"Error generating response: {e}"
                    st.error(bot_reply)

            st.session_state.messages.append(
                {"role": "assistant", "content": bot_reply}
            )