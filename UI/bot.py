import streamlit as st
import requests

# Define the Rasa server URL
RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"

st.title("Summer Semester Chatbot")

# Use session state to maintain the conversation history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Display the chat history
for message in st.session_state.chat_history:
    if message['sender'] == 'user':
        st.write(f"You: {message['message']}", unsafe_allow_html=True)
    else:
        st.write(f"Bot: {message['message']}", unsafe_allow_html=True)

# User input textbox
user_message = st.text_input("Type your message here...")

if st.button("Send"):
    # Add the user message to chat history
    st.session_state.chat_history.append({
        'sender': 'user',
        'message': user_message
    })

    # Send the user message to Rasa and get the bot's response
    payload = {
        "sender": "user",
        "message": user_message
    }

    response = requests.post(RASA_SERVER_URL, json=payload)
    rasa_response = response.json()

    # Extract the bot's message from the response
    bot_response = rasa_response[0]["text"] if rasa_response else "I couldn't process that message."

    # Add the bot's response to chat history
    st.session_state.chat_history.append({
        'sender': 'bot',
        'message': bot_response
    })

    # Refresh the page to show the updated chat history
    st.experimental_rerun()
