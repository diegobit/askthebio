import inspect

from pydantic import BaseModel

from .base_builder import BaseBuilder

class XResult(BaseModel):
    name: str
    x_handle: str
    bio: str
    website: str
    follower_count: str
    following_count: str
    posts: list[str]
    repost_and_like_summary: str
    profile_summary: str

class XBuilder(BaseBuilder):
    @staticmethod
    def name() -> str:
        return "x"

    @staticmethod
    def prompt(fullname, url, url_tag) -> str:
        return inspect.cleandoc(f"""
            Get personal information from {fullname} by reading the profile and some "tweets"/posts from x.com. The profile URL is {url}.

            Try to understand {fullname} from the most recent 10 updates, including posts, reposts, likes: if you see a post written by {fullname}, copy-paste it; if you see a repost or a like, try to understand what {fullname} seems to like.
        """)

    @staticmethod
    def controller_kwargs() -> dict:
        return {"output_model": XResult}

    @staticmethod
    def result_class() -> BaseModel:
        return XResult
