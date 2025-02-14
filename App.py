import dill
import streamlit as st
from langchain_groq import ChatGroq

# Load the function from the dill file
with open("groqcloud_function.dill", "rb") as f:
    query_groqcloud = dill.load(f)

# Streamlit UI configuration
st.set_page_config(page_title="All Ai chat", layout="wide")

# Title of the application
st.title("💬 All Ai chat")

# Layout configuration: Create a 2-column layout
col1, col2 = st.columns([1, 4])  # Model selection on the left, chat on the right

# Sidebar (model selection) on the left side in col1
with col1:
    model_name = st.selectbox(
        "Select a model", [
           "deepseek-r1-distill-llama-70b","deepseek-r1-distill-qwen-32b",
    "llama-3.3-70b-versatile",
    "llama-3.3-70b-specdec",
    "llama-3.2-1b-preview",
    "llama-3.2-3b-preview",
    "llama-3.1-8b-instant",
    "llama3-70b-8192",
    "llama3-8b-8192",
    "llama-guard-3-8b",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
    "llama-3.2-11b-vision-preview",
    "llama-3.2-90b-vision-preview"
        ], index=0
    )

# Chat history and chat input on the right side in col2
with col2:
    # Create a container for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chat container to hold the conversation
    with st.container():
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                # User messages are aligned to the right and colored black
                st.markdown(f'''
                <div style="background-color: #000000; color: white; padding: 10px 20px; border-radius: 12px; margin-bottom: 10px; max-width: 75%; text-align: right; word-wrap: break-word;">
                {msg["content"]}
                </div>''', unsafe_allow_html=True)
            else:
                # Assistant messages are aligned to the left and colored gray
                st.markdown(f'''
                <div style="background-color: #f1f1f1; color: black; padding: 10px 20px; border-radius: 12px; margin-bottom: 10px; max-width: 75%; text-align: left; word-wrap: break-word;">
                <div style="font-size: 0.85em; color: #888;">Model: {msg["content"]["model_name"]}</div>
                {msg["content"]["content"]}
                </div>''', unsafe_allow_html=True)

    # User input section (this will be below the chat history)
    user_input = st.chat_input("Ask me anything...")
    if user_input:
        # Display user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Get model response, passing the selected model name
        with st.spinner("Thinking..."):
            response,modelname = query_groqcloud(model_name, user_input)

        # Assuming the response is an object with .content and .model_name
        assistant_message = {
            "role": "assistant",
            "content": {
                "content": response,  # Accessing content property
                "model_name": modelname  # Accessing model_name property
            }
        }
        
        # Append the response to the message history
        st.session_state.messages.append(assistant_message)

        # Refresh the UI to show the new messages
        st.rerun()  # Use experimental_rerun to refresh the UI
