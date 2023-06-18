"""Util that calls Reddit."""
from typing import Any, Dict, Optional

from pydantic import BaseModel, Extra, root_validator

REDDIT_MAX_QUERY_LENGTH = 300

# Set up your Reddit API credentials
client_id = "lol"
client_secret = "lol"
user_agent = "python:harold:v1.0 (by /u/albagone)"


class RedditAPIWrapper(BaseModel):
    """Wrapper around RedditAPI.

    To use, you should have the ``praw`` python package installed.
    This wrapper will use the Reddit API to conduct searches and
    fetch post summaries
    """

    praw_client: Any  #: :meta private:
    top_k_posts: int = 3

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that the python package exists in environment."""
        try:
            import praw
            praw_client = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent,
            )

            values["praw_client"] = praw_client

        except ImportError:
            raise ValueError(
                "Could not import praw python package. "
                "Please install it with `pip install praw`."
            )
        return values

    def run(self, query: str) -> str:
        """Run Reddit search and get page summaries."""
        search_results = self.praw_client.subreddit("all").search(query[:REDDIT_MAX_QUERY_LENGTH])
        posts_and_comments = []
        iterator_in_lack_of_smarter_solution = 5
        if not search_results:
            return "No good Reddit Search Result was found"
        for reddit_post in search_results:
            iterator_in_lack_of_smarter_solution -= 1
            if not iterator_in_lack_of_smarter_solution:
                break
            summary = self.fetch_formatted_post_summary(reddit_post)
            if summary is not None:
                posts_and_comments.append(summary)
        return "\n\n".join(posts_and_comments)

    def fetch_formatted_post_summary(self, reddit_post: str) -> Optional[str]:
        try:
            comments = "..."
            if not reddit_post.num_comments:
                return None
                
            iterator_in_lack_of_smarter_solution = 5
            comments = ""
            for comment in reddit_post.comments.list():
                iterator_in_lack_of_smarter_solution -= 1
                if not iterator_in_lack_of_smarter_solution:
                    break
                comments += comment.body + "\n-------------------\n"

            return f"The following are top 3 posts and their top 5 comments:\nPost: {reddit_post.title}\nScore: {reddit_post.score}\nComments: {comments}"
        
        except Exception as e:
            print(e)
            return None
