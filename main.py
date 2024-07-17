import requests
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Load environment variables
load_dotenv()

# Now you can access the environment variables directly
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Function to fetch data from a route
def fetch_data_from_route(id):
    url = f'http://127.0.0.1:5000/users/{id}'  # Adjust the URL as needed
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

# Function to process the fetched data
def process_data(id):
    data = fetch_data_from_route(id)
    if data:
        return data
    else:
        print("Failed to fetch data from the route")
        return None

def chat_with_groq(processed_data, user_message):
    data_template = '''
        You are a helpful assistant. Here is the collected data:
        
        data: {data}
        Answer all questions based on this data to the best of your ability in {language}.
    '''
    prompt_description = "This is a chat interaction with an AI assistant using Groq."

    prom = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                data_template
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    store = {}

    model = ChatGroq(model="llama3-8b-8192")
    chain = prom | model

    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()
        return store[session_id]

    config = {"configurable": {"session_id": "abc4"}} # session_id could be the user id 

    with_message_history = RunnableWithMessageHistory(chain, get_session_history, input_messages_key="messages")

    response = with_message_history.invoke(
        {
            "data": processed_data,
            "messages": [HumanMessage(content=user_message)],
            "language": "English",
            "description": prompt_description
        },
        config=config
    )
    return response.content.strip('*').strip()  # Remove asterisks and extra whitespace

