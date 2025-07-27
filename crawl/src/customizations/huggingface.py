import inspect
from typing import Type

from pydantic import BaseModel, Field
from browser_use import Controller

from .base_customization import BaseCustomization


class HuggingFace(BaseCustomization):
    def __init__(
        self,
        name="huggingface",
        allowed_domains=["*.huggingface.co"],
        *args,
        **kwargs
    ) -> None:
        super().__init__(name=name, allowed_domains=allowed_domains, *args, **kwargs)

    def prompt(self, fullname: str) -> str:
        additional = ""
        if self.link.description:
            additional = f" {fullname} gave this additional information: {self.link.description}"

        return inspect.cleandoc(f"""
            Get information about {fullname} by crawling his/her huggingface repository. The URL to start is {self.link.url}.{additional}

            Check his posts, articles, collections, papers, models, datasets, spaces, etc, and extract overview information for the most recent of each (at least three per category):
              - Even if you don't crawl detailed information about everything, get the count of things he/she made, to understand at least how active {fullname} is.
              - If you can't find a section in {fullname}'s profile, that means the section is not present and {fullname} has 0 of that. Don't obsess about it.
              - For models, datasets, spaces, get the most recent and the ones with the most downloads (use the radio button to change the sorting). Make sure to keep only things made by {fullname}.

            Be thorough, truthful and factual.
        """)

    @staticmethod
    def controller() -> Controller:
        return Controller(
            output_model=HFResult
        )

    @staticmethod
    def result_class() -> Type[BaseModel]:
        return HFResult


# Result classes
class Activity(BaseModel):
    name: str
    date: str
    content_short_summary: str

class Reference(BaseModel):
    name: str
    url: str
    summary: str = Field(description="summary of readme/page content")

class ModelReference(BaseModel):
    name: str
    tag: str
    size: str
    updated_date: str
    downloads: int
    hearts: int
    summary: str = Field(description="summary of model readme")

class DatasetReference(BaseModel):
    name: str
    updated_date: str
    size: str
    downloads: int
    hearts: int
    summary: str = Field(description="summary of dataset readme")

class Stats(BaseModel):
    followers: int
    following: int
    n_posts: int
    n_articles: int
    n_collections: int
    n_papers: int
    n_models: int
    n_datasets: int

class HFResult(BaseModel):
    name: str
    username: str
    url: str
    ai_ml_interests: str
    recent_activity: list[Activity]
    organizations: list[str]
    stats: Stats
    posts: list[Reference]
    articles: list[Reference]
    collections: list[Reference]
    papers: list[Reference]
    models: list[ModelReference]
    datasets: list[DatasetReference]
    summary: str = Field(description="Summary of the profile: is the user active? What's the user's focus? What's the most important contribution?")
