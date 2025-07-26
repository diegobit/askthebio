import inspect
from typing import Type

from pydantic import BaseModel

from .base_builder import BaseBuilder

class Repo(BaseModel):
    name: str
    description: str
    stars: int
    languages: list[str]
    readme_summary: str
    code_overview: str
    other: str # TODO: keep?

class RepoRef(BaseModel):
    name: str
    author: str
    short_summary: str
    other: str# TODO: keep?

class SponsorRef(BaseModel):
    name: str
    id: str
    currently_active_sponsorship: bool
    sponsorship_amount: int
    other: str# TODO: keep?

class CodeRepoResult(BaseModel):
    username: str
    contact_info: list[str]
    bio: str
    achievements: str
    contributions_last_year: int
    repositories: list[Repo]
    most_recent_starred_projects: list[RepoRef]
    sponsoring_projects_or_users: list[SponsorRef]

class CodeRepoBuilder(BaseBuilder):
    @staticmethod
    def name() -> str:
        return "code_repo"

    @staticmethod
    def prompt(fullname, url, url_tag) -> str:
        return inspect.cleandoc(f"""
            Get information about what and how the code of {fullname} by crawling his/her repositories. The URL to start is {url}.

            Navigate the most popular or most recent (limit yourself to 50) repos, go inside the repo, read the README.md, navigate the hierarchy, and get high level information about each project.

            From this you will have to understand if {fullname} is writing a lot or a little open source code, which languages, what kind of projects, if he/she is spending effort into it, or not.
        """)

    @staticmethod
    def controller_kwargs() -> dict:
        return {"output_model": CodeRepoBuilder.result_class()}

    @staticmethod
    def allowed_domains() -> list[str]|None:
        return ["*.github.com", "*.uithub.com", "*.gitlab.com", "*.bitbucket.com"]

    @staticmethod
    def result_class() -> Type[BaseModel]:
        return CodeRepoResult

