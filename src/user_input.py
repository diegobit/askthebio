from pydantic import BaseModel

class Url(BaseModel):
    url: str
    url_tag: str|None

class UserInput(BaseModel):
    name: str
    urls: list[Url]

