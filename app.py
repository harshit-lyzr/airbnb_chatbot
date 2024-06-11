import streamlit as st
import os
from lyzr import QABot
import openai
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="Lyzr Airbnb Chatbot",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Lyzr Airbnb Chatbot")
st.markdown("### Welcome to the Lyzr Airbnb Chatbot!")
st.markdown("This app uses Lyzr QABot to assist with Airbnb properties. We have integrated Airbnb home informations and FAQs. Feel free to ask any questions related to Airbnb property.")
st.markdown("What is the wifi credentials?")
st.markdown("tell me rules of this airbnb?")

prompt=f"""
You are an Airbnb host with a welcoming, friendly, and attentive personality. 
You enjoy meeting new people and providing them with a comfortable and memorable stay. 
You have a deep knowledge of your local area and take pride in offering personalized recommendations. 
You are patient and always ready to address any concerns or questions with a smile. 
You ensure that your space is clean, cozy, and equipped with all the essentials. 
Your goal is to create a home away from home for your guests and to make their stay as enjoyable and stress-free as possible. 
When responding to guest questions, provide clear, helpful, and friendly answers based strictly on the provided data. 
[IMPORTANT]Do not give answers outside of the given information.
"""

@st.cache_resource
def rag_implementation():
    with st.spinner("Generating Embeddings...."):
        qa = QABot.pdf_qa(
            input_files=["/Users/harshitnariya/PycharmProjects/Lyzr/airbnb.pdf"],
            system_prompt=prompt

        )
    return qa


st.session_state["chatbot"] = rag_implementation()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if "chatbot" in st.session_state:
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = st.session_state["chatbot"].query(prompt)
            chat_response = response.response
            response = st.write(chat_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": chat_response}
        )