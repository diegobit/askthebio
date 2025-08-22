import asyncio
from browser_use import BrowserSession

async def manual_logins():
    session = BrowserSession(
        headless=False,
        # user_data_dir="~/.config/browseruse/profiles/my_profile",  # persists every cookie
        user_data_dir=None,
        storage_state="browser-use-auth-data.json",
        keep_alive=True
    )

    await session.start()
    page = await session.get_current_page()

    urls = [
        "https://github.com/login",
        "https://www.linkedin.com/login",
        "https://www.x.com",
        "https://huggingface.co/login"
    ]
    await page.goto(urls[0])
    for url in urls[1:]:
        tab = await session.browser_context.new_page()
        await tab.goto(url)

    print("Browser is ready – sign in everywhere, then ^C or close the window.")
    await asyncio.Event().wait()

    await session.save_storage_state("browser-use-auth-data.json")

asyncio.run(manual_logins())
