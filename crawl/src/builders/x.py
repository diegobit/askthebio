import inspect
from typing import Type

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
    repost_and_likes_summary: str
    profile_summary: str

class XBuilder(BaseBuilder):
    def __init__(self, url_desc: str = "x", name: str = "x") -> None:
        super().__init__(url_desc)

    @staticmethod
    def prompt(fullname, url, url_desc) -> str:
        return inspect.cleandoc(f"""
            Get personal information from {fullname} by reading the profile and some "tweets"/posts from x.com. The profile URL is {url}.

            Try to understand {fullname} interests, habits and ideas.

            Check the from the most recent 10 updates, including posts, reposts, likes
                - if you see a post written by {fullname}, copy-paste it
                - if you see a repost (also named 'You reposted') or a like, just make a summary.

            Be thorough, truthful and factual.
        """)

    @staticmethod
    def controller_kwargs() -> dict:
        return {"output_model": XBuilder.result_class()}

    @staticmethod
    def allowed_domains() -> list[str]|None:
        return ["*.x.com"]

    @staticmethod
    def result_class() -> Type[BaseModel]:
        return XResult
