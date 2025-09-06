from dotenv import load_dotenv

import asyncio

from src.models import Link, UserInput, Text
from src.crawl import crawl_user

async def main():
    user = UserInput(
        name="Diego Giorgini",
        texts=[
        ],
        docs=[],
        links=[
            Link(url="https://www.linkedin.com/in/diego-giorgini", description=""),
            Link(url="https://www.github.com/diegobit/", description=""),
            Link(url="https://www.x.com/diegobit10", description=""),
            Link(url="https://www.huggingface.co/diegobit", description=""),
            Link(url="https://diegobit.com", description="personal website"),
        ]
    )

    await crawl_user(user, out_path="out", verbose=True)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
