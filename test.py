from langchain.agents import initialize_agent
from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.chains import LLMBashChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper
from langchain.utilities import GoogleSerperAPIWrapper
from reddit_tool import RedditSearchTool as Reddit
from reddit_util import RedditAPIWrapper

openai_api_key = "lol"

llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
tools = [Reddit(
    api_wrapper=RedditAPIWrapper()
)]


memory = ConversationBufferMemory(memory_key="chat_history")
agent_chain = initialize_agent(tools, llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True, memory=memory)

agent_chain.run(input="Summarize what people think about king Charles")
