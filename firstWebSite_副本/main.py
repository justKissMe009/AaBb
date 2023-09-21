import streamlit as st
from langchain.utilities import SQLDatabase

from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain_experimental.sql import SQLDatabaseChain

with st.sidebar:
    openai_api_key = st.text_input("ANDY'S OpenAI", key="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", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/2_Chat_with_search.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("🔎 AaBb Data Analysis - Chat with search")

"""
In this page, we're using Open AI to dive into the data in Our AaBb Data Platform with an interactive 🤝 way.
Try more with our platform  🤝 and you can reach out to Team AaBb for any questions :-).
"""

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search your dataset. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Who won the Women's U.S. Open in 2018?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True)
    """
    SQL DATABASE ANALYSIS
    """
    db = SQLDatabase.from_uri("sqlite:///Chinook.db")
    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

    st.write(db_chain.run("How many employees are there?"))

    search = DuckDuckGoSearchRun(name="Search")
    search_agent = initialize_agent([search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True)
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)