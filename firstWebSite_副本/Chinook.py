from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
# from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI
from langchain_experimental.sql import SQLDatabaseChain

openai_api_key = "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"
db = SQLDatabase.from_uri("sqlite:///Chinook.db")


agent_executor = create_sql_agent(
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key, verbose=True),
    toolkit=SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0)),
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

agent_executor.run(
    "List the total sales per country. Which country's customers spent the most?"
)