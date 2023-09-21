from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI
from langchain_experimental.sql import SQLDatabaseChain


openai_api_key ="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"

db = SQLDatabase.from_uri("sqlite:///Chinook.db")
llm = OpenAI(temperature=0, openai_api_key=openai_api_key, verbose=True)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

db_chain.run("How many employees are there?")