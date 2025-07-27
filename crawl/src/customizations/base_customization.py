import os
from pydantic import BaseModel
from typing import Type

from browser_use import Controller


class BaseCustomization():
    def __init__(
        self,
        link,
        name: str = "base",
        allowed_domains: list[str]|None = None,
        max_steps: int = 250,
        out_path: str = "out"
    ) -> None:
        self.link = link
        self.name = name
        self.allowed_domains = allowed_domains
        self.max_steps = max_steps
        self.out_path = os.path.join(out_path, self.name)

    def prompt(self, *args, **kwargs) -> str:
        raise NotImplementedError

    @staticmethod
    def controller(*args, **kwargs) -> Controller:
        raise NotImplementedError

    @staticmethod
    def result_class(*args, **kwargs) -> Type[BaseModel]:
        raise NotImplementedError
