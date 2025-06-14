import streamlit as st
from openai import OpenAI
import os

# --- Configuration ---
# You can set your OpenAI API key here.
# For local development, you can replace "YOUR_OPENAI_API_KEY_HERE" with your actual key,
# or set it as an environment variable (e.g., OPENAI_API_KEY=sk-...).
# For deployment on Streamlit Community Cloud, use st.secrets["OPENAI_API_KEY"].
# It's recommended to use environment variables or Streamlit secrets for security.
# Example using environment variable:
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Example using Streamlit secrets:
# client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))
# For this example, we'll use a placeholder for direct input, but please use secrets/env vars for real apps.

# Initialize the OpenAI client. Replace the API key placeholder with your actual key
# or ensure it's loaded from st.secrets or environment variables.
# If you are running locally and setting it directly:
# client = OpenAI(api_key="YOUR_OPENAI_API_KEY_HERE")
# If using Streamlit secrets (recommended for deployment):
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY="sk-YOUR_ACTUAL_OPENAI_API_KEY_GOES_HERE"", os.getenv("OPENAI_API_KEY")))

st.set_page_config(page_title="Simple AI Chatbot", layout="centered")

st.title("🗣️ Simple AI Chatbot")
st.markdown("---")

# --- Chat History Management ---
# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    # Use st.chat_message to display messages with appropriate roles (user/assistant)
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input ---
# Create a chat input widget at the bottom of the app
if prompt := st.chat_input("What's on your mind?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in the chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- AI Response Generation ---
    # Display a placeholder for the assistant's response while it's being generated
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # Call OpenAI's chat completions API
            # The 'messages' argument takes a list of message dictionaries.
            # We pass the entire chat history for conversational context.
            # 'stream=True' allows us to display the response as it's being generated.
            for chunk in client.chat.completions.create(
                model="gpt-3.5-turbo", # You can choose other models like "gpt-4" if you have access
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                # Append the new content chunk to the full response
                full_response += chunk.choices[0].delta.content or ""
                # Update the placeholder with the current full response and a blinking cursor
                message_placeholder.markdown(full_response + "▌")
            # After the response is complete, display the final full response
            message_placeholder.markdown(full_response)
        except Exception as e:
            # Handle potential errors during API call (e.g., invalid API key, network issues)
            st.error(f"An error occurred: {e}. Please check your API key and try again.")
            full_response = "I encountered an error trying to generate a response. Please try again."
            message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- Sidebar for Controls ---
with st.sidebar:
    st.header("Chat Controls")
    # Button to clear the chat history
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        # Rerun the app to reflect the cleared history immediately
        st.experimental_rerun()

    st.markdown("---")
    st.markdown("### How to use:")
    st.markdown("- Type your message in the input box below.")
    st.markdown("- Press Enter or click the send icon.")
    st.markdown("- The AI's response will appear above.")
    st.markdown("- Click 'Clear Chat History' to start a new conversation.")
    st.markdown("---")
    st.markdown("Powered by OpenAI and Streamlit")
