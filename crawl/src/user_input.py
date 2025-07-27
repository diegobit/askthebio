from pydantic import BaseModel

class Link(BaseModel):
    url: str
    description: str = ""

class Text(BaseModel):
    title: str
    content: str

class Doc(BaseModel):
    title: str
    ref: str # TODO: implement

class UserInput(BaseModel):
    name: str
    links: list[Link]
    texts: list[Text]
    docs: list[Doc]

