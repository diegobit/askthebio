from pydantic import BaseModel

class Url(BaseModel):
    url: str
    description: str = ""

class UserInput(BaseModel):
    name: str
    urls: list[Url]

