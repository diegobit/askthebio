import inspect
from typing import Type

from pydantic import BaseModel
from browser_use import Controller

from .base_customization import BaseCustomization


class Linkedin(BaseCustomization):
    def __init__(
        self,
        name="linkedin",
        allowed_domains=["*.linkedin.com"],
        *args,
        **kwargs
    ) -> None:
        super().__init__(name=name, allowed_domains=allowed_domains, *args, **kwargs)

    def prompt(self, fullname: str) -> str:
        return inspect.cleandoc(f"""
            Get all information from {fullname} from his/her LinkedIn profile. Start from URL {self.link.url}.

            Extract his/her profession, experiences, education, certifications, etc. Check out the most recent 10 updates, including posts, reposts, etc
              - if you see a post by {fullname}, download it.
              - if you see a repost, only make a summary.

            Be thorough, truthful and factual.
        """)

    @staticmethod
    def controller() -> Controller:
        return Controller(
            output_model=LinkedinResult
        )

    @staticmethod
    def result_class() -> Type[BaseModel]:
        return LinkedinResult


# Result classes
class LinkedinPersonalInfo(BaseModel):
    name: str
    job_title: str
    linkedin_url: str
    current_work_position: str
    sector: str
    user_bio: str
    location: str
    email: str
    phone_number: str
    website: str
    others: list[str]

class LinkedinExperience(BaseModel):
    job_title: str
    company: str
    employment_type: str
    duration_or_dates: str
    summary: str

class LinkedinEducation(BaseModel):
    education_title: str
    university_or_school_name: str
    course_name: str
    duration_or_dates: str
    activities_and_associations: str
    description: str

class LinkedinCertification(BaseModel):
    name: str
    emitting_organization: str
    course_name: str
    date_concession: str
    url: str
    description: str

class LinkedinResult(BaseModel):
    personal_info: LinkedinPersonalInfo
    experience: list[LinkedinExperience]
    education: list[LinkedinEducation]
    certifications: list[LinkedinCertification]
    skills: list[str]
    posts: list[str]
    reposts: list[str]
    interests: str
    profile_summary: str
