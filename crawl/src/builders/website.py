import inspect
from typing import Type

from pydantic import BaseModel, Field

from .base_builder import BaseBuilder

class PageChunk(BaseModel):
    title_or_tag: str = Field("one/two word description of the chunk")
    snippet: str

class Page(BaseModel):
    url: str
    tag: str = Field(description="One of: 'personal_website', 'online_cv', 'article_about_the_user', 'article_written_by_the_user', 'social_page', 'other'")
    content_snippets: list[PageChunk]
    page_summary: str

class PageResult(BaseModel):
    root_url: str
    root_tag: str = Field(description="One of: 'personal_website', 'online_cv', 'article_about_the_user', 'article_written_by_the_user', 'social_page', 'other'")
    relevant_contents: list[PageChunk]
    children: list[Page] = Field(description="Flat list of all relevant pages (children) of the root page.")
    overall_summary: str

class WebsiteBuilder(BaseBuilder):
    def __init__(self, url_tag: str = "a website", name: str = "website") -> None:
        super().__init__(url_tag)
        self.name = name

    @staticmethod
    def prompt(fullname, url, url_tag) -> str:
        return inspect.cleandoc(f"""
            I'm gathering all personal information from {fullname} to build a comprehensive profile. I'm equally interested in factual knowledge about {fullname} and in getting to know {fullname} as a person.

            Your task is to crawl this website: {url}. The website is tagged as "{url_tag}".

            Always check whether a /llms.txt file exists: that will give you a good look on the hierarchy of the website.

            Do not write in the final result object any consideration about the extraction; only put information about {fullname}.

            Be thorough, truthful and factual.
        """)

    @staticmethod
    def controller_kwargs() -> dict:
        return {"output_model": WebsiteBuilder.result_class()}

    @staticmethod
    def allowed_domains() -> list[str]|None:
        return None

    @staticmethod
    def result_class() -> Type[BaseModel]:
        return PageResult
