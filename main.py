from __future__ import annotations
import os
import inspect
import json
from pydantic import BaseModel, Field
from typing import Dict, List, Optional

from dotenv import load_dotenv

load_dotenv()

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
    others: List[str]

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
    experience: List[LinkedinExperience]
    education: List[LinkedinEducation]
    certifications: List[LinkedinCertification]
    skills: List[str]
    posts: List[str]
    interests: str
    profile_summary: str

class XResult(BaseModel):
    name: str
    x_handle: str
    bio: str
    website: str
    follower_count: str
    following_count: str
    posts: List[str]
    repost_and_like_summary: str
    profile_summary: str

class PageChunk(BaseModel):
    title_or_tag: str = Field("one/two word description of the chunk")
    content: str

class Page(BaseModel):
    url: str
    tag: str = Field(description="One of: 'personal_website', 'online_cv', 'article_about_the_user', 'article_written_by_the_user', 'social_page', 'other'")
    relevant_contents: list[PageChunk]
    summary: str

class PageResult(BaseModel):
    root_url: str
    root_tag: str = Field(description="One of: 'personal_website', 'online_cv', 'article_about_the_user', 'article_written_by_the_user', 'social_page', 'other'")
    relevant_contents: list[PageChunk]
    children: list[Page] = Field(description="Flat list of all relevant pages (children) of the root page.")
    overall_summary: str

# def linkedin_scraper():
#     from linkedin_scraper import Person, actions
#     from selenium import webdriver
#     driver = webdriver.Chrome()
#     email = os.environ['EMAIL']
#     password = os.environ['PASSWORD']
#     actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
#     person = Person("https://www.linkedin.com/in/diego-giorgini", driver=driver)
#     # print("Hello from diegobit-ai!")
#     # # Process the same files shown in the demo
#     # linkedin = Attachments("https://www.linkedin.com/in/diego-giorgini?")
#     # print(f"linkeidn: {len(str(linkedin))}")
#     import code; code.interact(local=dict(globals(), **locals()))

def attachments_pdf():
    from attachments import Attachments
    pdf = Attachments("https://code.ics.uci.edu/wp-content/uploads/2020/06/Resume-Sample-1-Software-Engineer.pdf")
    import code; code.interact(local=dict(globals(), **locals()))

def docling_pdf():
    from docling.document_converter import DocumentConverter
    source = "https://code.ics.uci.edu/wp-content/uploads/2020/06/Resume-Sample-1-Software-Engineer.pdf"  # document per local path or URL
    converter = DocumentConverter()
    result = converter.convert(source)
    with open("out_docling.md", "w") as f:
        f.write(result.document.export_to_markdown())

prompt_website = inspect.cleandoc("""
    I'm gathering all personal information from Diego Giorgini to build a comprehensive profile. I'm equally interested in factual knowledge about Diego and in getting to know Diego as a person.

    Your task is to crawl this website: https://diegobit.com. The website is tagged as "personal website".

    Always check whether a /llms.txt file exists: that will give you a good look on the hierarchy of the website.

    Do not write in the final result object any consideration about the extraction; only put information about Diego.
""")

prompt_linkedin = inspect.cleandoc("""
    Get all information from Diego Giorgini from his/her LinkedIn profile. Start from https://www.linkedin.com/in/diego-giorgini.

    Extract his profession, experiences, education, certifications, etc. Check out the most recent 10 updates, including posts, reposts, etc: if you see a post, download it.
""")

    # Access the personal profile at https://www.linkedin.com/in/diego-giorgini, you should already be logged in with difigi@icloud.com, if not, use t*T\\gi,{2K~m3=b=J?4=C9,]XEg8DY

prompt_x = inspect.cleandoc("""
    Get personal information from Diego Giorgini by reading the profile and some "tweets"/posts from X.com. The profile link is https://x.com/diegobit10

    Try to understand him/her from the most recent 10 updates, including posts, reposts, likes: if you see a post written by Diego, copy-paste it; if you see a repost or a like, try to understand what Diego seems to like.
""")

def browser_use(mode: str, prompt: str, out_path: str):
    import asyncio
    from browser_use import Agent, BrowserSession, Controller
    from browser_use.llm import ChatGoogle

    os.makedirs(os.path.join(out_path, "logs/conversation"), exist_ok=True)
    browser_session = BrowserSession(
        headless=False,
        storage_state='~/.cache/playwright_data.json'
    )

    async def main():
        if mode == "linkedin":
            controller = Controller(output_model=LinkedinResult)
        elif mode == "x":
            controller = Controller(output_model=XResult)
        else:
            controller = Controller(output_model=PageResult)

        agent = Agent(
            task=prompt,
            llm=ChatGoogle(model=os.environ['MODEL'], temperature=0.3),
            controller=controller,
            browser_session=browser_session,
            downloads_path=out_path,
            save_conversation_path=os.path.join(out_path, "logs/conversation")
        )
        history = await agent.run(max_steps=25)
        history.save_to_file(os.path.join(out_path, "history.json"))

        result = history.final_result()
        if result:
            if mode == "linkedin":
                parsed = LinkedinResult.model_validate_json(result)
            elif mode == "x":
                parsed = XResult.model_validate_json(result)
            else:
                parsed = PageResult.model_validate_json(result)

            print(parsed)
            with open(os.path.join(out_path, "extraction.json"), "w", encoding="utf-8") as f:
                f.write(parsed.model_dump_json(indent=2))

        else:
            print('No result')

    asyncio.run(main())

if __name__ == "__main__":
    # linkedin_scraper()
    # attachments_pdf()
    # docling_pdf()
    # browser_use(mode="x", prompt=prompt_x, out_path="out_x")
    # browser_use(mode="linkedin", prompt=prompt_linkedin, out_path="out_linkedin") 
    browser_use(mode="website", prompt=prompt_website, out_path="out_website")
