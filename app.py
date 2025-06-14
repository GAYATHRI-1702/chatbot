import streamlit as st
from openai import OpenAI
import os # Useful for fallback to environment variables

# Initialize the OpenAI client using st.secrets.
# It's good practice to also allow loading from environment variables for flexibility
# (e.g., if you run locally without a secrets.toml but with an env var).
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except KeyError:
    # Fallback to environment variable if not found in st.secrets (e.g., if running outside Streamlit Cloud and no secrets.toml)
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        client = OpenAI(api_key=api_key)
    else:
        st.error("OpenAI API key not found. Please configure it in .streamlit/secrets.toml or as an environment variable.")
        st.stop() # Stop the app if API key is missing

st.title("🗣️ AI Chatbot")

# ... rest of your chatbot code ...
# (The rest of the code from the previous example remains largely the same)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What's on your mind?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            for chunk in client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response += chunk.choices[0].delta.content or ""
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"An error occurred: {e}. Please check your API key and try again.")
            full_response = "I encountered an error trying to generate a response. Please try again."
            message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

with st.sidebar:
    st.header("Chat Controls")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.experimental_rerun()

    st.markdown("---")
    st.markdown("### How to use:")
    st.markdown("- Type your message in the input box below.")
    st.markdown("- Press Enter or click the send icon.")
    st.markdown("- The AI's response will appear above.")
    st.markdown("- Click 'Clear Chat History' to start a new conversation.")
    st.markdown("---")
    st.markdown("Powered by OpenAI and Streamlit (API key securely managed)")