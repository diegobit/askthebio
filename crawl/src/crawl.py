import os
import subprocess
import time
import shutil
import contextlib
import asyncio
import json
from urllib.parse import urlparse
from types import CoroutineType
from datetime import datetime
import inspect
import  unicodedata
import re

from browser_use import Agent, Browser, BrowserProfile
from browser_use.llm import ChatGoogle

from src.models import Link, UserInput, Text, Doc
from src.customizations import CodeRepo, GitHub, Linkedin, Website, X, HuggingFace

from loguru import logger

def slugify(text: str) -> str:
    # Normalize (NFKC keeps characters in canonical form)
    text = unicodedata.normalize("NFKC", text)
    # Lowercase (works for many scripts, e.g. Greek, Cyrillic, Latin)
    text = text.lower()
    # Replace any character that's not a letter/number with a hyphen
    text = re.sub(r"[^\w]+", "-", text, flags=re.UNICODE)
    # Strip leading/trailing hyphens
    text = text.strip("-")
    # Collapse multiple hyphens
    text = re.sub(r"-{2,}", "-", text)
    return text

def detect_profile_name(chrome_user_dir: str) -> str:
    ls_path = os.path.join(chrome_user_dir, "Local State")
    try:
        with open(ls_path, "r", encoding="utf-8") as f:
            ls = json.load(f)
        return ls.get("profile", {}).get("last_used", "Default")
    except Exception:
        return "Default"

async def crawl_user(
    user: UserInput,
    out_path: str,
    concurrency: int = 5,
    verbose: bool = False
):
    final_result = {}
    final_md = f"# {user.name}\n\n"

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
    # TODO: 

    # ---------------------------------
    # START BROWSERS
    # ---------------------------------
    chrome_exec_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    chrome_user_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome/")
    profile_name = detect_profile_name(chrome_user_dir)
    ports = [p for p in list(range(9222, 9222+concurrency))]
    browsers: list[Browser] = []
    chrome_tmp_dirs = []

    for p in ports:
        logger.info(f"Starting browser on port: {p}.")
        cdp_url = f"http://127.0.0.1:{p}"
        chrome_tmp_dir = f"/tmp/askthebio-profiles/{p}"
        chrome_tmp_dirs.append(chrome_tmp_dir)
        # copy profile dir
        shutil.copytree(
            src=os.path.join(chrome_user_dir, profile_name),
            dst=os.path.join(chrome_tmp_dir, profile_name),
            symlinks=True,
            copy_function=shutil.copy2,
            dirs_exist_ok=True
        )
        assert os.path.exists(os.path.join(chrome_tmp_dir, profile_name, "Bookmarks")), "Profile copy failed"

        # start browser
        subprocess.Popen(
            [
                chrome_exec_path,
                f"--remote-debugging-port={p}",
                f"--user-data-dir={chrome_tmp_dir}",
                f"--profile-directory={profile_name}",
                "--no-first-run",
                "--no-default-browser-check",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(1) # TODO: improve waiting
        # connect browser-use
        # profile = BrowserProfile(minimum_wait_page_load_time=0.1, wait_between_actions=0.1)
        br = Browser(cdp_url=cdp_url, headless=False)#, browser_profile=profile, headless=False)
        await br.start()
        browsers.append(br)

    browser_pool: asyncio.Queue[Browser] = asyncio.Queue()
    for br in browsers:
        await browser_pool.put(br)

    running_agents: list[CoroutineType] = []

    # ---------------------------------
    # Run an agent for each url
    # ---------------------------------
    logger.info("Start crawling.")
    for link in user.links:
        netloc = urlparse(link.url).netloc.replace("www.", "")

        # Make builder for specific website
        if netloc == "github.com":
            logger.info(f"Processing {link.url} as GitHub")
            agent_builder = GitHub(link=link, name="github")

        elif "gitlab" in netloc or "bitbucket" in netloc:
            logger.info(f"Processing {link.url} as Other code repo")
            agent_builder = CodeRepo(link=link)

        elif netloc == "huggingface.co":
            logger.info(f"Processing {link.url} as Huggingface")
            agent_builder = HuggingFace(link=link)

        elif netloc == "linkedin.com":
            logger.info(f"Processing {link.url} as Linkedin")
            agent_builder = Linkedin(link=link)

        elif netloc == "x.com":
            logger.info(f"Processing {link.url} as X")
            agent_builder = X(link=link)

        else:
            logger.info(f"Processing {link.url} as Website")
            agent_builder = Website(link=link)

        # Make browser-use controller
        controller = agent_builder.controller()

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
            browser_session=None,
            downloads_path=out_path,
            save_conversation_path=logs_path
        )

        # Add agent coroutine to gather async coroutines
        async def run_agent_w_builder(agent, max_steps, builder, pool: asyncio.Queue):
            # take a free browser
            window = await pool.get()
            try:
                agent.browser_session = window
                history = await agent.run(max_steps=max_steps)
                return history, builder
            finally:
                # return the browser to the pool so the next job can use it
                await pool.put(window)

        running_agents.append(
            run_agent_w_builder(agent, agent_builder.max_steps, agent_builder, browser_pool)
        )

    # Wait for agents to finish and save results to file
    for coro_agent in asyncio.as_completed(running_agents):
        history, agent_builder = await coro_agent

        if verbose:
            history.save_to_file(os.path.join(agent_builder.out_path, "history.json"))

        result = history.final_result()
        if result:
            parsed = agent_builder.result_class().model_validate_json(result)
            parsed_j = parsed.model_dump()
            parsed_j["knowledge_cutoff_date"] = datetime.isoformat(datetime.now()),
            final_result[agent_builder.name] = parsed_j
            final_md += f"## {agent_builder.name}\n"
            final_md += "```json\n"
            final_md += f"{json.dumps(parsed_j, indent=2)}\n"
            final_md += "```\n\n"
            if verbose:
                logger.info(parsed_j)
            json.dump(parsed_j, open(os.path.join(agent_builder.out_path, "extraction.json"), "w"))
        else:
            logger.info(f'No result from {agent_builder.link.url}')
            final_result[agent_builder.name] = {}

    # Save to file
    slug_name = slugify(user.name)
    with open(os.path.join(out_path, f"{slug_name}.json"), "w") as f:
        json.dump(final_result, f, indent=2)
    with open(os.path.join(out_path, f"{slug_name}.md"), "w") as f:
        f.write(final_md)

    # Close all the browsers
    for br in browsers:
        with contextlib.suppress(Exception):
            await br.stop()

    # Clean tmp dirs
    for tmp in chrome_tmp_dirs:
        shutil.rmtree(tmp, ignore_errors=True)

