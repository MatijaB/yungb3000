from langchain.agents import initialize_agent
from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.chains import LLMBashChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from reddit_tool import RedditQueryRun
from reddit_util import RedditAPIWrapper

openai_api_key = "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"

llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
tools = [RedditQueryRun(
    api_wrapper=RedditAPIWrapper()
)]

memory = ConversationBufferMemory(memory_key="chat_history")
agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)

agent_chain.run(input="What do people on Reddit think about OpenAI causing the end of the world?")
