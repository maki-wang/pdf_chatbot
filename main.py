# -*- coding: utf-8 -*-
# @Time    : 2024/8/14 00:47
# @Author  : Maki Wang
# @FileName: main.py
# @Software: PyCharm
# !/usr/bin/env python3

import streamlit as st
from utils import qa_agent
from langchain.memory import ConversationBufferMemory

st.title("AI-powered PDF Q&A tool")

with st.sidebar:
    openai_api_key = st.text_input("Please enter the OpenAI API key:", type="password")
    st.markdown("[Get OpenAI API key](https://platform.openai.com/account/api-keys)")
    st.markdown("---")
    st.write("Designed by Xianmu, please contact via ***wangxianmu@gmail.com***")

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(
        return_messages=True,
        memory_key="chat_history",
        output_key="answer"
    )

uploaded_file = st.file_uploader("Upload your PDF file:", type="pdf")
question = st.text_input("Ask questions about the content of the PDF here:", disabled=not uploaded_file)

if uploaded_file and question and not openai_api_key:
    st.info("Please enter the OpenAI API key!")
if uploaded_file and question and openai_api_key:
    with st.spinner("AI is thinking, please wait..."):
        response = qa_agent(openai_api_key, st.session_state['memory'], uploaded_file, question)
    st.write("### Answer:")
    st.write(response["answer"])
    st.session_state["chat_history"] = response["chat_history"]

if "chat_history" in st.session_state:
    with st.expander("**Chat History**"):
        for i in range(0, len(st.session_state["chat_history"]), 2):
            human_message = st.session_state["chat_history"][i]
            ai_message = st.session_state["chat_history"][i+1]
            st.chat_message('human').write(human_message.content)
            st.chat_message('ai').write(ai_message.content)
            if i < len(st.session_state["chat_history"]) - 2:
                st.divider()