import os
import asyncio
from urllib.parse import urlparse
from typing import Type
from pydantic import BaseModel

from browser_use import Agent, BrowserSession, Controller
from browser_use.llm import ChatGoogle

from user_input import Url, UserInput
from builders import CodeRepoBuilder, LinkedinBuilder, WebsiteBuilder, XBuilder, HFBuilder

async def browser_use(
    prompt: str,
    controller_args: dict,
    result_class: Type[BaseModel],
    out_path: str,
    max_steps: int = 25,
    verbose: bool = False
):
    logs_path = None
    if verbose:
        logs_path = os.path.join(out_path, "logs/conversation")
        os.makedirs(logs_path, exist_ok=True)

    browser_session = BrowserSession(
        headless=False,
        # storage_state='~/.cache/playwright_data.json'
        user_data_dir='~/.config/browseruse/profiles/my_profile'
    )

    controller = Controller(**controller_args)

    agent = Agent(
        task=prompt,
        llm=ChatGoogle(
            model=os.environ['MODEL'],
            temperature=0.3,
            thinking_budget=0,
        ),
        controller=controller,
        browser_session=browser_session,
        downloads_path=out_path,
        save_conversation_path=logs_path
    )

    history = await agent.run(max_steps=max_steps)

    if verbose:
        history.save_to_file(os.path.join(out_path, "history.json"))

    result = history.final_result()
    if result:
        parsed = result_class.model_validate_json(result)
        print(parsed)
        with open(os.path.join(out_path, "extraction.json"), "w", encoding="utf-8") as f:
            f.write(parsed.model_dump_json(indent=2))
    else:
        print('No result')


async def main():
    user_input = UserInput(
        name="Julien Chaumond",
        urls=[
            # Url(url="https://www.linkedin.com/in/diego-giorgini", url_tag=None),
            # Url(url="https://www.github.com/diegobit", url_tag=None),
            # Url(url="https://www.x.com/diegobit10", url_tag=None),
            Url(url="https://huggingface.co/julien-c", url_tag=None),
            # Url(url="https://diegobit.com", url_tag="personal website"),
        ]
    )

    results = []

    for url_obj in user_input.urls:
        if "github" in url_obj.url or "gitlab" in url_obj.url:
            builder = CodeRepoBuilder()
            url_tag = "code_repo"
        elif "linkedin" in url_obj.url:
            builder = LinkedinBuilder()
            url_tag = "linkedin"
        elif "x" in url_obj.url:
            builder = XBuilder()
            url_tag = "x"
        else:
            builder = WebsiteBuilder()
            url_tag = url_obj.url_tag
            # TODO: implement

        results.append(
            browser_use(
                prompt=builder.prompt(user_input.name, url_obj.url, url_tag),
                controller_args=builder.controller_kwargs(),
                result_class=builder.result_class(),
                max_steps=25,
                out_path=os.path.join("out", builder.name()),
                verbose=True
            )
        )

    for res in results:
        await res

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    asyncio.run(main())
