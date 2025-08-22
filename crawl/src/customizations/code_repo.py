import inspect
from typing import Type

from pydantic import BaseModel
import requests
from browser_use import Controller, ActionResult

from .base_customization import BaseCustomization


class CodeRepo(BaseCustomization):
    def __init__(
        self,
        name: str = "code_repo",
        allowed_domains: list[str]|None = ["*.github.com", "*.uithub.com", "*.gitlab.com", "*.bitbucket.com"],
        *args,
        **kwargs
    ) -> None:
        super().__init__(name=name, allowed_domains=allowed_domains, *args, **kwargs)

    def prompt(self, fullname: str) -> str:
        return inspect.cleandoc(f"""
            Get information about what and how the code of {fullname} by crawling his/her repositories. The URL to start is {self.link.url}.

            About repos:
            - Gather detailed information about 5/10 repos among the pinned ones, the most popular and the most recently updated repos of {fullname} (into repositories_detailed object): Get the overview from the README.md; if unavailable, or you need more information, use `get_github_code` function to get in a single step a the first lines of each file in the repo.
            - For all other repos, Only gather basic information (repositories_basic object).
            - Ignore private repositories, keep public ones.

            Be thorough, truthful and factual.
        """)

    @staticmethod
    def controller() -> Controller:
        return Controller(
            output_model=CodeRepoResult
        )

    @staticmethod
    def result_class() -> Type[BaseModel]:
        return CodeRepoResult


class GitHub(CodeRepo):
    @staticmethod
    def controller() -> Controller:
        controller = CodeRepo.controller()

        @controller.registry.action('Get GitHub code summary')
        def get_github_code(repo_url: str) -> ActionResult:
            uithub_url = repo_url.replace("github.com", "uithub.com")
            uithub_url = f"{uithub_url}?accept=text%2Fplain&maxTokens=10000"
            response = requests.get(uithub_url)
            return ActionResult(extracted_content=response.text, include_in_memory=False)

        return controller


# Result classes
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
