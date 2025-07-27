import os
import asyncio
import json
from urllib.parse import urlparse
from types import CoroutineType
from datetime import datetime

from browser_use import Agent, BrowserSession, BrowserProfile
from browser_use.llm import ChatGoogle

from user_input import Link, UserInput, Text, Doc
from customizations import CodeRepo, GitHub, Linkedin, Website, X, HuggingFace


async def crawl_user(
    user: UserInput,
    out_path: str,
    verbose: bool = False
):
    final_result = {}

    # ---------------------------------
    # TEXTS
    # ---------------------------------
    for text in user.texts:
        final_result[text.title] = text.content

    # ---------------------------------
    # DOCS
    # ---------------------------------
    # TODO: implement
    # for doc in user.docs:
    #     ...

    # ---------------------------------
    # LINKS
    # ---------------------------------
    running_agents: list[CoroutineType] = []

    # Run an agent for each url
    for link in user.links:
        netloc = urlparse(link.url).netloc.replace("www.", "")

        # Make builder for specific website
        if netloc == "github.com":
            print(f"Processing {link.url} as GitHub")
            agent_builder = GitHub(link=link, name="github")

        elif "gitlab" in netloc or "bitbucket" in netloc:
            print(f"Processing {link.url} as Other code repo")
            agent_builder = CodeRepo(link=link)

        elif netloc == "huggingface.co":
            print(f"Processing {link.url} as Huggingface")
            agent_builder = HuggingFace(link=link)

        elif netloc == "linkedin.com":
            print(f"Processing {link.url} as Linkedin")
            agent_builder = Linkedin(link=link)

        elif netloc == "x.com":
            print(f"Processing {link.url} as X")
            agent_builder = X(link=link)

        else:
            print(f"Processing {link.url} as Website")
            agent_builder = Website(link=link)

        # Make browser-use controller
        controller = agent_builder.controller()

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
            allowed_domains=agent_builder.allowed_domains,
        )
        await window.start()

        # Start browser-use agent
        logs_path = None
        if verbose:
            logs_path = os.path.join(agent_builder.out_path, "logs/conversation")
            os.makedirs(logs_path, exist_ok=True)

        agent = Agent(
            task=agent_builder.prompt(user.name),
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
            run_agent_w_builder(agent, agent_builder.max_steps, agent_builder)
        )

    # Wait for agents to finish and save results to file
    for coro_agent in asyncio.as_completed(running_agents):
        history, agent_builder = await coro_agent

        if verbose:
            history.save_to_file(os.path.join(agent_builder.out_path, "history.json"))

        result = history.final_result()
        if result:
            parsed = agent_builder.result_class().model_validate_json(result)
            parsed_j = parsed.model_dump_json(indent=2)
            parsed_j["knowledge_cutoff_date"] = datetime.isoformat(datetime.now()),
            final_result[agent_builder.name] = parsed_j
            if verbose:
                print(parsed_j)
            with open(os.path.join(agent_builder.out_path, "extraction.json"), "w", encoding="utf-8") as f:
                f.write(parsed_j)
        else:
            print(f'No result from {agent_builder.link.url}')
            final_result[agent_builder.name] = {}

    with open(os.path.join(out_path, "merged_results.json"), "w") as f:
        json.dump(final_result, f, indent=2)



async def main():
    user = UserInput(
        name="Diego Giorgini",
        texts=[
        ],
        docs=[],
        links=[
            Link(url="https://www.linkedin.com/in/diego-giorgini", description=""),
            Link(url="https://www.github.com/diegobit/aranet4-mcp-server", description=""),
            Link(url="https://www.x.com/diegobit10", description=""),
            Link(url="https://www.huggingface.co/diegobit", description=""),
            Link(url="https://diegobit.com", description="personal website"),
        ]
    )

    await crawl_user(user, out_path="out", verbose=True)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    asyncio.run(main())
