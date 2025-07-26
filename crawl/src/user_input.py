from pydantic import BaseModel

class Url(BaseModel):
    url: str
    url_tag: str = ""

class UserInput(BaseModel):
    name: str
    urls: list[Url]

