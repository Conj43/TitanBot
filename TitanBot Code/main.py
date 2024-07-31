# to run this application: streamlit run main.py

# imports
import os
import tempfile
from dotenv import load_dotenv
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import requests
import sqlite3

# langchain imports
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents import create_tool_calling_agent
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.chat_history import BaseChatMessageHistory

# load env variables
load_dotenv()

# define open ai api key
openai_api_key = os.environ['OPENAI_API_KEY']

# imports from other files
from utils import call_agent
from prompts import full_prompt
from tools import create_map_llm, create_tools
from ui import display_chat_messages, get_user_query, setup_streamlit_page, clear_message_history


# sets up streamlit page in ui.py
setup_streamlit_page()


# Initialize session state variables
if "db_path" not in st.session_state:
    st.session_state.db_path = None

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

if "store" not in st.session_state:
    st.session_state.store = {}

# Sidebar content
if st.sidebar.button("Clear History"):
    clear_message_history()
st.sidebar.subheader("Welcome to our Transportation Database Assistant!")
st.sidebar.markdown("First, upload your database with traffic or accident information, then chat with your data! \
                    You can map your data by asking DataBot to map accidents or crashes with specific queries. \
                    You can also visualize your data by asking DataBot to graph queried data for you!")
st.sidebar.markdown("---")
st.sidebar.subheader("Database Upload")
st.sidebar.markdown("Upload a SQLite .db file for analysis.")
uploaded_file = st.sidebar.file_uploader("Choose a database file", key="bottom_uploader")

# Handle file upload
if uploaded_file is not None:
    if uploaded_file.name.endswith('.db'):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name
        temp_file.close()
        st.session_state.db_path = temp_file_path
        st.sidebar.success("Database uploaded successfully.") 
    else:
        st.sidebar.error("Error: The uploaded file is not a .db file. Please try a .db file.")

# Function to fetch data from URL and save as SQLite .db file
def fetch_data_and_create_db(url, db_file_path):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        conn = sqlite3.connect(db_file_path)
        cursor = conn.cursor()

        # Assuming data['active'] is a list of dictionaries
        if 'active' in data:
            sample_row = data['active'][0]
            columns = sample_row.keys()

            # Create table dynamically
            column_definitions = ', '.join([f"{col} TEXT" for col in columns])
            create_table_sql = f"CREATE TABLE IF NOT EXISTS traffic_data ({column_definitions})"
            cursor.execute(create_table_sql)

            # Insert data dynamically
            for row in data['active']:
                columns = ', '.join(row.keys())
                placeholders = ', '.join(['?'] * len(row))
                sql = f"INSERT INTO traffic_data ({columns}) VALUES ({placeholders})"
                cursor.execute(sql, list(row.values()))

            conn.commit()
            conn.close()
            return db_file_path
        else:
            st.sidebar.error("Error: JSON does not contain 'active' key.")
            return None
    else:
        st.sidebar.error(f"Error: Unable to fetch data from URL. Status code: {response.status_code}")
        return None

# Option to input a URL for data
st.sidebar.markdown("Or, provide a URL to fetch data:")
data_url = st.sidebar.text_input("Enter URL")

# Handle URL input
if st.sidebar.button("Fetch Data"):
    if data_url:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_file_path = temp_file.name
        temp_file.close()
        db_path = fetch_data_and_create_db(data_url, temp_file_path)
        if db_path:
            st.session_state.db_path = db_path
            st.sidebar.success("Data fetched and database created successfully.")
    else:
        st.sidebar.error("Error: Please provide a valid URL.")

# Initialize db connection to your .db file
if st.session_state.db_path is not None:
    db_url = URL.create( 
        drivername="sqlite",
        database=st.session_state.db_path,
        query={"mode": "ro"}
    )
    engine = create_engine(db_url)
    db = SQLDatabase(engine)

    # Method to get chat history for current session id in store
    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in st.session_state.store:
            st.session_state.store[session_id] = ChatMessageHistory()
        return st.session_state.store[session_id]



    # method to create sql agent with history 
    def create_sql_agent_with_history(db, tools, full_prompt):
        agent = create_sql_agent( # initilaize sql agent
            llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
            db=db,
            prompt=full_prompt,
            verbose=True,
            agent_type="openai-tools",
            extra_tools=tools,
            # return_intermediate_steps=True,
            max_iterations=10,
        )
        

        agent_with_chat_history = RunnableWithMessageHistory( # init runnable with history
            agent,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

        return agent_with_chat_history # return the runnable agent with chat history


    # initialize tools from tools.py function 
    tools = create_tools(st.session_state.db_path)

    # create the agent with chat history
    agent_with_chat_history = create_sql_agent_with_history(db, tools, full_prompt)

    # create map llm which interprets whether or not to use map 
    map_llm = create_map_llm()

    # displays past messages
    display_chat_messages(st.session_state["messages"])

    # gets the users input 
    user_query = get_user_query()

    # if user has submitted input
    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query}) # add the input to messages
        st.chat_message("user", avatar="💬").write(user_query)

        with st.chat_message("assistant", avatar="🤖"):
            st_cb = StreamlitCallbackHandler(st.container()) # use built in langchain function to get call backs to display to container
            config = {"configurable": {"session_id": "123"}, "callbacks": [st_cb]} # initialize config with session id and st_cb is streamlit callbacks
            response = call_agent(user_query, config, agent_with_chat_history) # get the response
            response = response['output'] # just keep the output text from the bot
            st.session_state.messages.append({"role": "assistant", "content": response}) # add output to the end of the messages
            st.write(response) # write it to the screen

            
