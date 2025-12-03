<!-- LOGO -->
<h1>
<p align="center">
  <img src="https://askthebio.diegobit.com/favicon.ico" alt="Logo" width="128">
  <br>Ask The Bio
</h1>
</p>

This repo holds the code of a proof of concept for the AI Biographer!

Read the [accompanying article!](https://diegobit.com/post/ask-the-bio)

[Try it out](https://askthebio.diegobit.com) asking stuff about me 🙈.

### crawl/

Extract information from your socials/personal blogs into a JSON or markdown file.

### agent/

The agent service which receives the user question and routes the request to Gemini. Ready to be deployed as a CloudFlare Worker.

### gui/

The static website with the input prompt. Ready to be deployed as a CloudFlare Page.
