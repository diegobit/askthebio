import inspect
from typing import Type

from pydantic import BaseModel
from browser_use import Controller

from .base_customization import BaseCustomization


class X(BaseCustomization):
    def __init__(
        self,
        name="x",
        allowed_domains=["*.x.com"],
        *args,
        **kwargs
    ) -> None:
        super().__init__(name=name, allowed_domains=allowed_domains, *args, **kwargs)

    def prompt(self, fullname) -> str:
        return inspect.cleandoc(f"""
            Get personal information from {fullname} by reading the profile and some "tweets"/posts from x.com. The profile URL is {self.link.url}.

            Try to understand {fullname} interests, habits and ideas.

            Check the from the most recent 10 updates, including posts, reposts, likes
                - if you see a post written by {fullname}, copy-paste it
                - if you see a repost (also named 'You reposted') or a like, just make a summary.

            Be thorough, truthful and factual.
        """)

    @staticmethod
    def controller() -> Controller:
        return Controller(
            output_model=XResult
        )

    @staticmethod
    def result_class() -> Type[BaseModel]:
        return XResult


# Result classes
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
