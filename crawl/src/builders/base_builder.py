import os
from pydantic import BaseModel
from typing import Type

class BaseBuilder():
    name = "base"

    def __init__(self, url_tag: str = "", out_path: str = "out") -> None:
        self.url_tag = url_tag
        self.out_path = os.path.join(out_path, self.name)

    @staticmethod
    def prompt(fullname: str, url: str, url_tag: str, *args, **kwargs) -> str:
        raise NotImplementedError

    @staticmethod
    def controller_kwargs(*args, **kwargs) -> dict:
        raise NotImplementedError

    @staticmethod
    def result_class(*args, **kwargs) -> Type[BaseModel]:
        raise NotImplementedError

    @staticmethod
    def allowed_domains() -> list[str]|None:
        raise NotImplementedError

    @staticmethod
    def max_steps(n: int = 250) -> int:
        return n
