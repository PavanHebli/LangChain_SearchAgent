from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_groq import ChatGroq
import os
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
import streamlit as st

st.title('AskMe Anything.')
option = st.selectbox(
    "Select the API provider ",
    ("No Selection", "Groq", "OpenAI")
)
llm_api = st.text_input("Enter API Key", type="password")
tavily_api = st.text_input("Enter Tavily Api", type="password")
source_text = st.text_area("Type your Question", height=50)
if st.button("Find Out"):
    if not llm_api.strip() or not source_text.strip():
        st.write(f"Please complete the missing fields.")
    else:
        os.environ["TAVILY_API_KEY"] = tavily_api
        search = TavilySearchResults(max_results=2)
        # search_results = search.invoke(source_text)
        # st.write(search_results[0]["content"])
        # st.write(search_results)
        tools = [search]
        model = ChatGroq(model="llama3-8b-8192", api_key=llm_api)
        # response = model.invoke([HumanMessage(content=source_text)])
        # response.content
        # model_with_tools = model.bind_tools(tools)
        agent_executor = create_react_agent(model, tools)
        response = agent_executor.invoke({"messages": [HumanMessage(content=source_text)]})
        st.write(response["messages"][-1].content)
        del os.environ['TAVILY_API_KEY']

