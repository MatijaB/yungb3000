"""Tool for the Reddit API."""

from typing import Optional

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools.base import BaseTool
from reddit_util import RedditAPIWrapper


class RedditSearchTool(BaseTool):
    """Tool that adds the capability to search using the Reddit API."""

    name = "Intermediate Answer"
    description = (
        "A wrapper around Reddit. "
        "Useful for when you need to answer general questions about "
        "what people are talking about or what people think about certain topics. "
        "Input should be up to 3 words. The input should never be more than 3 words."
    )
    api_wrapper: RedditAPIWrapper

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Reddit tool."""
        return self.api_wrapper.run(query)

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Reddit tool asynchronously."""
        raise NotImplementedError("RedditQueryRun does not support async")