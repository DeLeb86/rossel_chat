from openai import OpenAI
import re
import os
from config import *
import streamlit as st
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")
print(st.secrets.keys())
pre_prompt=open(prompt_path).read()
x=st.secrets["key"]
st.title("News Buddy")
client = OpenAI(api_key=x)
st.session_state["model"]=model
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role" : "system", "content" : "Tu es un assistant qui résumé l'actualité"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What article do you want to summarize ?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content":  "Fais-moi un résumé de cette article en quelques lignes :" + prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

with st.chat_message("assistant"):
    stream = client.chat.completions.create(
        model=st.session_state["model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )
    response = st.write_stream(stream)
st.session_state.messages.append({"role": "assistant", "content": response})


    