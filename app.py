import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from context import TWIN_SYSTEM_PROMPT
from tools import tools, handle_tool_calls

load_dotenv(override=True)

MODEL_NAME = "gpt-5.4-mini"

openai = OpenAI()

system = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}]


st.set_page_config(
    page_title="Digital Twin",
    page_icon="🤖"
)

st.title("Digital Twin")
st.write("Talk to my AI twin about my career")


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


if prompt := st.chat_input("Talk to my AI twin..."):

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    messages = system + st.session_state.messages

    response = openai.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=tools
    )

    while response.choices[0].finish_reason == "tool_calls":

        message = response.choices[0].message
        tool_calls = message.tool_calls

        results = handle_tool_calls(tool_calls)

        messages.append(message)
        messages.extend(results)

        response = openai.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools
        )

    answer = response.choices[0].message.content

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.write(answer)
