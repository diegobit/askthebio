from pydantic import BaseModel

class Link(BaseModel):
    url: str
    description: str = ""

class UserInput(BaseModel):
    name: str
    links: list[Link]

