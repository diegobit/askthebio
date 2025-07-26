import inspect
from typing import Type

from pydantic import BaseModel, Field

from .base_builder import BaseBuilder

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

class HFBuilder(BaseBuilder):
    def __init__(self, url_tag: str = "huggingface", name: str = "huggingface") -> None:
        super().__init__(url_tag)
        self.name = name

    @staticmethod
    def prompt(fullname, url, url_tag) -> str:
        additional = ""
        if url_tag:
            additional = f" {fullname} gave this additional information: {url_tag}"

        return inspect.cleandoc(f"""
            Get information about {fullname} by crawling his/her huggingface repository. The URL to start is {url}.{additional}

            Check his posts, articles, collections, papers, models, datasets, spaces, etc, and extract overview information for the most recent of each (at least three per category). It's not important to have everything, but what you get should be perfectly accurate. Even if you don't crawl detailed information about everything, get the count of things he/she made, to understand at least how active {fullname} is. Not every section could be present in {fullname}'s profile: that means he/she has 0 of that.

            For models, datasets, spaces, get the most recent and the ones with the most downloads (use the radio button to change the sorting). Make sure to keep only things made by {fullname}.

            Be thorough, don't end until you have everything you need.
        """)

    @staticmethod
    def controller_kwargs() -> dict:
        return {"output_model": HFBuilder.result_class()}

    @staticmethod
    def allowed_domains() -> list[str]|None:
        return ["*.huggingface.co"]

    @staticmethod
    def result_class() -> Type[BaseModel]:
        return HFResult

