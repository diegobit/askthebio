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
    last_update: str
    license: str
    last_commit: str
    other: str

class RepoRef(BaseModel):
    name: str
    author: str
    short_summary: str

class SponsorRef(BaseModel):
    name: str
    id: str
    currently_active_sponsorship: bool
    sponsorship_amount: int

class CodeRepoResult(BaseModel):
    username: str
    company: str
    location: str
    personal_bio: str
    email: str
    socials: str
    achievements: str
    contributions_last_year: int
    repositories_detailed: list[Repo]
    repositories_basic: list[RepoRef]
    other_people_starred_repos: list[RepoRef]
    sponsoring_projects_or_users: list[SponsorRef]
    profile_summary: str

class CodeRepoBuilder(BaseBuilder):
    def __init__(self, url_desc: str = "code_repo", name: str = "code_repo") -> None:
        super().__init__(url_desc)
        self.name = name

    @staticmethod
    def prompt(fullname, url, url_desc) -> str:
        return inspect.cleandoc(f"""
            Get information about what and how the code of {fullname} by crawling his/her repositories. The URL to start is {url}.

            About repos:
            - Gather detailed information about 5/10 repos among the pinned ones, the most popular and the most recently updated repos of {fullname} (into repositories_detailed object): Get the overview from the README.md; if unavailable, or you need more information, use `get_github_code` function to get in a single step a the first lines of each file in the repo.
            - For all other repos, Only gather basic information (repositories_basic object).

            Be thorough, truthful and factual.
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
