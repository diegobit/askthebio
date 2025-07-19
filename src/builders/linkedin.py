import inspect

from pydantic import BaseModel

from .base_builder import BaseBuilder

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
    interests: str
    profile_summary: str

class LinkedinBuilder(BaseBuilder):
    @staticmethod
    def name() -> str:
        return "linkedin"

    @staticmethod
    def prompt(fullname, url, url_tag) -> str:
        return inspect.cleandoc(f"""
            Get all information from {fullname} from his/her LinkedIn profile. Start from URL {url}.

            Extract his/her profession, experiences, education, certifications, etc. Check out the most recent 10 updates, including posts, reposts, etc: if you see a post, download it.
        """)

    @staticmethod
    def controller_kwargs() -> dict:
        return {"output_model": LinkedinResult}

    @staticmethod
    def result_class() -> BaseModel:
        return LinkedinResult

