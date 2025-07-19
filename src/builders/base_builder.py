from pydantic import BaseModel

class BaseBuilder():
    @staticmethod
    def name() -> str:
        raise NotImplementedError

    @staticmethod
    def prompt(fullname: str, url: str, url_tag: str, *args, **kwargs) -> str:
        raise NotImplementedError

    @staticmethod
    def controller_kwargs(*args, **kwargs) -> dict:
        raise NotImplementedError

    @staticmethod
    def result_class(*args, **kwargs) -> BaseModel:
        raise NotImplementedError

