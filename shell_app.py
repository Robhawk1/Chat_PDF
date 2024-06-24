from langchain.llms import OpenAI
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st
from langchain_community.tools import ShellTool
from langchain.agents import AgentType, initialize_agent
from langchain_openai import ChatOpenAI
#from langchain.llms import ChatGoogleGenerativeAI
import getpass, os
#from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage

os.environ['OPENAI_API_KEY'] = 
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] =


shell_tool = ShellTool()


llm = ChatOpenAI(temperature=0)

shell_tool.description = shell_tool.description + f"args {shell_tool.args}".replace(
    "{", "{{"
).replace("}", "}}")
agent = initialize_agent(
    [shell_tool], llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True, handle_parsing_errors=True,
)

if "history" not in st.session_state:
    st.session_state.history = []

def message_history_to_string(extra_space: bool=True) -> str:
    """
    Return a string of the chat history contained in
    st.session_state.history.
    """

    history_list = []
    for msg in st.session_state.history:
        if isinstance(msg, HumanMessage):
            history_list.append(f"Human: {msg.content}")
        else:
            history_list.append(f"AI: {msg.content}")
    new_lines = "\n\n" if extra_space else "\n"

    return new_lines.join(history_list)

if prompt := st.chat_input():
    st.chat_message("human").write(prompt)
    with st.chat_message("ai"):
        st_callback = StreamlitCallbackHandler(st.container())

        chat_history = message_history_to_string()
        history_query = {
        "chat_history": chat_history,
        "input": prompt,
        }
        response = agent.run(history_query, callbacks=[st_callback])
        human_message = HumanMessage(content=prompt)
        st.session_state.history.append(human_message)
        st.session_state.history.append(AIMessage(content=response))
        st.write(response)
