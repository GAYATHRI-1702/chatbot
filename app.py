import streamlit as st
import time # Used for simulating AI "thinking" time

st.set_page_config(page_title="Mock AI Chatbot", layout="centered")

st.title("🤖 Mock AI Chatbot")
st.markdown("---")

# --- Chat History Management ---
# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add an initial greeting from the assistant
    st.session_state.messages.append({"role": "assistant", "content": "Hello! I'm a simple mock AI. Ask me anything, or try saying 'hello' or 'how are you?'"})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input ---
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in the chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- Mock AI Response Generation ---
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Simulate a small delay for AI "thinking"
        time.sleep(0.5)

        # Simple rule-based responses for the mock AI
        if "hello" in prompt.lower() or "hi" in prompt.lower():
            response_text = "Hello there! How can I help you today?"
        elif "how are you" in prompt.lower():
            response_text = "I'm just a program, so I don't have feelings, but I'm functioning perfectly! How about you?"
        elif "your name" in prompt.lower():
            response_text = "I don't have a name. I am a mock AI designed to show Streamlit's chat capabilities."
        elif "weather" in prompt.lower():
            response_text = "I can't tell you the weather right now, as I don't have access to real-time information!"
        elif "bye" in prompt.lower() or "goodbye" in prompt.lower():
            response_text = "Goodbye! It was nice chatting with you (virtually, of course)."
        elif "streamlit" in prompt.lower():
            response_text = "Streamlit is an amazing Python library for creating web apps for data science and machine learning!"
        else:
            response_text = f"You said: '{prompt}'. I'm a simple mock AI and can't understand complex queries. Try asking something simpler!"

        # Simulate streaming the response
        for char in response_text:
            full_response += char
            message_placeholder.markdown(full_response + "▌") # Add a blinking cursor
            time.sleep(0.02) # Small delay for typing effect

        message_placeholder.markdown(full_response) # Display final response without cursor

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- Sidebar for Controls ---
with st.sidebar:
    st.header("Chat Controls")
    # Button to clear the chat history
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        # Add the initial greeting again after clearing
        st.session_state.messages.append({"role": "assistant", "content": "Hello! I'm a simple mock AI. Ask me anything, or try saying 'hello' or 'how are you?'"})
        st.experimental_rerun() # Rerun the app to clear the displayed messages

    st.markdown("---")
    st.markdown("### About this app:")
    st.markdown("This is a mock AI chatbot built with Streamlit. It uses pre-programmed responses and **does not connect to any external AI models or require API keys/secrets.**")
    st.markdown("It demonstrates the basic chat interface features of Streamlit.")
    st.markdown("---")
    st.markdown("Simulated AI by Streamlit")
