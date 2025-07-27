import inspect
from typing import Type

from pydantic import BaseModel, Field
from browser_use import Controller

from .base_customization import BaseCustomization


class Website(BaseCustomization):
    def __init__(
        self,
        name="website",
        *args,
        **kwargs
    ) -> None:
        super().__init__(name=name, *args, **kwargs)

    def prompt(self, fullname) -> str:
        additional = ""
        if self.link.description:
            additional = f"The website is tagged as '{self.link.description}'"

        return inspect.cleandoc(f"""
            I'm gathering all personal information from {fullname} to build a comprehensive profile. I'm equally interested in factual knowledge about {fullname} and in getting to know {fullname} as a person.

            Your task is to crawl this website: {self.link.url}. {additional}

            Always check whether a /llms.txt file exists: that will give you a good look on the hierarchy of the website.

            Do not write in the final result object any consideration about the extraction; only put information about {fullname}.

            Be thorough, truthful and factual.
        """)

    @staticmethod
    def controller() -> Controller:
        return Controller(
            output_model=WebsiteResult
        )

    @staticmethod
    def result_class() -> Type[BaseModel]:
        return WebsiteResult


# Result classes
class PageChunk(BaseModel):
    title_or_tag: str = Field("one/two word description of the chunk")
    snippet: str

class Page(BaseModel):
    url: str
    tag: str = Field(description="One of: 'personal_website', 'online_cv', 'article_about_the_user', 'article_written_by_the_user', 'social_page', 'other'")
    content_snippets: list[PageChunk]
    page_summary: str

class WebsiteResult(BaseModel):
    root_url: str
    root_tag: str = Field(description="One of: 'personal_website', 'online_cv', 'article_about_the_user', 'article_written_by_the_user', 'social_page', 'other'")
    relevant_contents: list[PageChunk]
    children: list[Page] = Field(description="Flat list of all relevant pages (children) of the root page.")
    overall_summary: str
