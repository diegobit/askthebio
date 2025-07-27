import os
import asyncio
from urllib.parse import urlparse
from types import CoroutineType

import requests
from browser_use import Agent, BrowserSession, Controller, BrowserProfile, ActionResult
from browser_use.llm import ChatGoogle

from user_input import Url, UserInput
from builders import CodeRepoBuilder, LinkedinBuilder, WebsiteBuilder, XBuilder, HFBuilder


async def crawl_user(
    user: UserInput,
    out_path: str,
    verbose: bool = False
):
    running_agents: list[CoroutineType] = []

    # Run an agent for each url
    for link in user.urls:
        netloc = urlparse(link.url).netloc.replace("www.", "")

        # Make builder for specific website
        if netloc == "github.com":
            print(f"Processing {link.url} as GitHub")
            builder = CodeRepoBuilder(name="github")

        elif "gitlab" in netloc or "bitbucket" in netloc:
            print(f"Processing {link.url} as Other code repo")
            builder = CodeRepoBuilder()

        elif netloc == "huggingface.co":
            print(f"Processing {link.url} as Huggingface")
            builder = HFBuilder()

        elif netloc == "linkedin.com":
            print(f"Processing {link.url} as Linkedin")
            builder = LinkedinBuilder()

        elif netloc == "x.com":
            print(f"Processing {link.url} as X")
            builder = XBuilder()

        else:
            print(f"Processing {link.url} as Website")
            builder = WebsiteBuilder(url_desc=link.description)
            controller = Controller(**builder.controller_kwargs())

        # Make browser-use controller
        controller = Controller(**builder.controller_kwargs())

        if builder.name == "github":
            @controller.registry.action('Get GitHub code summary')
            def get_github_code(repo_url: str) -> ActionResult:
                uithub_url = repo_url.replace("github.com", "uithub.com")
                uithub_url = f"{uithub_url}?accept=text%2Fplain&maxTokens=10000"
                response = requests.get(uithub_url)
                return ActionResult(extracted_content=response.text, include_in_memory=False)

        # Make browser-use profile to load auth data
        shared_profile = BrowserProfile(
            headless=False,
            user_data_dir=None,               # use dedicated tmp user_data_dir per session
            storage_state='browser-auth-data.json',   # load/save cookies to/from json file
            keep_alive=False
        )

        # Create browser window
        window = BrowserSession(
            browser_profile=shared_profile,
            allowed_domains=builder.allowed_domains(),
        )
        await window.start()

        # Start browser-use agent
        logs_path = os.path.join(builder.out_path, "logs/conversation")
        os.makedirs(logs_path, exist_ok=True)

        agent = Agent(
            task=builder.prompt(user.name, link.url, link.description),
            llm=ChatGoogle(
                model=os.environ['MODEL'],
                temperature=0.3,
                thinking_budget=0,
            ),
            controller=controller,
            browser_session=window,
            downloads_path=out_path,
            save_conversation_path=logs_path
        )

        # Add agent coroutine to later gather
        async def run_agent_w_builder(agent, max_steps, builder):
            history = await agent.run(max_steps=max_steps)
            return history, builder

        running_agents.append(
            run_agent_w_builder(agent, builder.max_steps(), builder)
        )

    # Wait for agents to finish and save results to file
    for coro_agent in asyncio.as_completed(running_agents):
        history, builder = await coro_agent

        if verbose:
            history.save_to_file(os.path.join(builder.out_path, "history.json"))

        result = history.final_result()
        if result:
            parsed = builder.result_class().model_validate_json(result)
            print(parsed)
            with open(os.path.join(builder.out_path, "extraction.json"), "w", encoding="utf-8") as f:
                f.write(parsed.model_dump_json(indent=2))
        else:
            print('No result')



async def main():
    user = UserInput(
        name="Diego Giorgini",
        urls=[
            Url(url="https://www.linkedin.com/in/diego-giorgini", description=""),
            Url(url="https://www.github.com/diegobit/aranet4-mcp-server", description=""),
            Url(url="https://www.x.com/diegobit10", description=""),
            Url(url="https://www.huggingface.co/diegobit", description=""),
            Url(url="https://diegobit.com", description="personal website"),
        ]
    )

    await crawl_user(user, out_path="out", verbose=True)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    asyncio.run(main())
