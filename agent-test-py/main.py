import inspect
from dotenv import load_dotenv
import logfire
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModelSettings
from pydantic_ai.models.gemini import ThinkingConfig
import asyncio
import streamlit as st

if "agent_init" not in st.session_state:
    load_dotenv()

    logfire.configure()
    logfire.instrument_pydantic_ai()
    st.session_state["agent_init"] = True

settings = GeminiModelSettings(
    gemini_thinking_config=ThinkingConfig(
        include_thoughts=False,
        thinking_budget=0
    )
)

class Output(BaseModel):
    answer: str

context = """{
"my bio from veronica": "Diego is the best friend of all animals",
"github": {
  "knowledge_cutoff_date": "2025-06-27",
  "username": "diegobit",
  "company": "AI Technologies SRL",
  "location": "Italy",
  "personal_bio": "Hi, I'm Diego! Welcome to my page 👋\n👨‍💻 I'm an Italian programmer based in La Spezia. I'm currently leading technical development at AI Technologies. I hold an MS in Computer Science (AI focus) from the University of Pisa.\n🌐 Check out my old-school website, made from scratch without any framework! Drop me an email to tell me if you like it!",
  "email": "hello@diegobit.com",
  "socials": "diegobit.com, @diegobit10, huggingface.co/diegobit",
  "achievements": "None listed on the page.",
  "contributions_last_year": 1174,
  "repositories_detailed": [
    {
      "name": "aranet4-mcp-server",
      "description": "SImple MCP server to manage your aranet4 device and local db.",
      "stars": 4,
      "languages": [
        "Python"
      ],
      "readme_summary": "The 'aranet4-mcp-server' is a simple Multi-Client Protocol (MCP) server designed to manage Aranet4 CO2 sensors and store their data in a local database. It leverages the Aranet4-Python library to scan for devices, fetch data, and save it to an SQLite database. Key features include scanning, data fetching, and querying recent/historical measurements. The project is under active development, with recent commits focusing on README updates, improved error handling, and configuration fixes.",
      "code_overview": "The repository is primarily written in Python and uses the Aranet4-Python library. It includes a `main.py` for server operations, `db.py` for database interactions, and `config.py` for configuration. The `requirements.txt` lists dependencies like `aranet4-python`, `fastapi`, and `uvicorn`. The code structure suggests a modular design for managing Aranet4 devices and data storage.",
      "last_update": "Jun 5, 2024",
      "license": "Not specified",
      "other": "Recent commits indicate ongoing development with updates to README, better date/sensor error handling, and configuration fixes. Key files include main.py, db.py, config.py, requirements.txt, smithery.yaml, uv.lock."
    },
    {
      "name": "dotfiles",
      "description": "Dotfiles for zsh, neovim, vscode, ghostty, kitty, karabiner, aerospace. Mostly MacOS specific. GNU Stow as farm manager.",
      "stars": 2,
      "languages": [
        "Shell"
      ],
      "readme_summary": "The 'dotfiles' repository contains configuration files and a script for setting up a new MacOS device. It manages configurations for various applications like zsh, neovim, vscode, ghostty, kitty, karabiner, and aerospace. GNU Stow is used for managing these dotfiles. The repository is primarily focused on MacOS.",
      "code_overview": "The repository contains shell scripts and configuration files for various applications. It uses GNU Stow for managing symbolic links to the dotfiles. Key files and directories include `.config`, `.vscode/extensions`, `Library/Application Support/Code/User`, and specific configuration files for applications like aerospace, Powerlevel10k, and tmux.",
      "last_update": "May 25, 2024",
      "license": "Not specified",
      "other": "The repository is mostly MacOS specific and uses GNU Stow as a 'farm manager' for dotfiles."
    },
    {
      "name": "diegobit",
      "description": "This is a special repository whose `README.md` will appear on Diego's public profile.",
      "stars": 0,
      "languages": [],
      "readme_summary": "The 'diegobit/diegobit' repository is a special GitHub repository whose `README.md` content appears on the owner's public profile. It serves as a personal introduction page for Diego, an Italian programmer. The repository itself does not contain a project or application, but rather personal information and a link to an external website.",
      "code_overview": "This repository primarily consists of a `README.md` file that serves as a personal introduction. It does not contain any functional code or project files. Its purpose is purely for displaying profile information on GitHub.",
      "last_update": "May 25, 2024",
      "license": "Not specified",
      "other": "This repository is a special GitHub repository for the user's profile README."
    }
  ],
  "repositories_basic": [
    {
      "name": "aranet4-mcp-server",
      "author": "diegobit",
      "short_summary": "SImple MCP server to manage your aranet4 device and local db."
    },
    {
      "name": "dotfiles",
      "author": "diegobit",
      "short_summary": "Dotfiles for zsh, neovim, vscode, ghostty, kitty, karabiner, aerospace. Mostly MacOS specific. GNU Stow as farm manager."
    },
    {
      "name": "diegobit",
      "author": "diegobit",
      "short_summary": "This is a special repository whose `README.md` will appear on Diego's public profile."
    },
    {
      "name": "c-course-salvatore",
      "author": "diegobit",
      "short_summary": "code snippets for the c course from Salvatore Sanfilipo"
    },
    {
      "name": "url2llm",
      "author": "diegobit",
      "short_summary": "The easiest way to crawl a website and produce LLM ready markdown files, paying only your LLM provider via API"
    },
    {
      "name": "advent_of_code_2024",
      "author": "diegobit",
      "short_summary": "Learning Go with Advent of Code 2024"
    },
    {
      "name": "lotus58-lily58-layout",
      "author": "diegobit",
      "short_summary": "Layout explanation and .vil files of my lotus58 and lily58"
    },
    {
      "name": "aranet4-archiver",
      "author": "diegobit",
      "short_summary": "Python scripts to periodically update a db with co2 measures from aranet4 sensor and to plot the history."
    },
    {
      "name": "kitty-icon",
      "author": "diegobit",
      "short_summary": "An Alternative icon for kitty terminal."
    },
    {
      "name": "colima-alfred-workflow",
      "author": "diegobit",
      "short_summary": "A simple Alfred worflow to check the status of colima, start and stop it"
    },
    {
      "name": "coreGPT",
      "author": "karpathy",
      "short_summary": "Keras 3 conversion of nanoGPT repo: \"The simplest, fastest repository for training/finetuning medium-sized GPTs.\""
    },
    {
      "name": "usa-plus",
      "author": "diegobit",
      "short_summary": "A USA MacOS layout with easy accented characters."
    },
    {
      "name": "DRIPS",
      "author": "diegobit",
      "short_summary": "Decentralized Relative Inertial Positioning System"
    },
    {
      "name": "OSX-ASUS-UX32A",
      "author": "diegobit",
      "short_summary": "Everything needed to boot OS X on an ASUS UX32A"
    },
    {
      "name": "PCalc-Hybrid-Layout",
      "author": "diegobit",
      "short_summary": "An RPN layout for PCalc"
    },
    {
      "name": "Drawing-And-Rolling",
      "author": "diegobit",
      "short_summary": "A little physics based game for OS X"
    },
    {
      "name": "SoundNotes",
      "author": "diegobit",
      "short_summary": "An Android text editor with audio recordings"
    },
    {
      "name": "DistractionFreeWindow",
      "author": "aziz",
      "short_summary": "SublimeText \"Distraction free mode\" but not full-screen! A windowed UI is more manageable and accessible yet it can be simple and sublime!"
    }
  ],
  "most_recent_starred_projects": [
    {
      "name": "coreGPT",
      "author": "karpathy",
      "short_summary": "Keras 3 conversion of nanoGPT repo: \"The simplest, fastest repository for training/finetuning medium-sized GPTs.\""
    }
  ],
  "sponsoring_projects_or_users": [],
  "profile_summary": "Diego Giorgini is an Italian programmer leading technical development at AI Technologies SRL. He holds an MS in Computer Science with an AI focus from the University of Pisa. His GitHub profile showcases 1,174 contributions in the last year. He has a personal website and is active on Twitter and Hugging Face. His pinned repositories include 'url2llm', 'aranet4-mcp-server', 'aranet4-archiver', 'Prompt to improve ChatGPT websearch', 'coreGPT', and 'dotfiles'."
},
"website": {
  "knowledge_cutoff_date": "2025-06-27",
  "root_url": "https://diegobit.com",
  "root_tag": "personal_website",
  "relevant_contents": [
    {
      "title_or_tag": "Initial Information",
      "content": "Diego Giorgini is an italian programmer passionate with AI and based in La Spezia."
    }
  ],
  "children": [
    {
      "url": "https://diegobit.com/about",
      "tag": "personal_website",
      "relevant_contents": [
        {
          "title_or_tag": "Current Role",
          "content": "AI Engineer, leading technical development at AI Technologies"
        },
        {
          "title_or_tag": "Location",
          "content": "La Spezia, Italy"
        },
        {
          "title_or_tag": "Education",
          "content": "MS in Computer Science (AI focus) from University of Pisa, advised by Professor Davide Bacciu, with a thesis on Recurrent Neural Networks."
        },
        {
          "title_or_tag": "Interests",
          "content": "Indie videogames (especially single-player, short, unique experiences), Classic literature, Mechanical keyboards"
        },
        {
          "title_or_tag": "Social Media Profiles",
          "content": "Email: hello@diegobit.com, GitHub: https://github.com/diegobit, X (Twitter): https://x.com/diegobit10, LinkedIn: https://www.linkedin.com/in/diegogiorgini/, Hugging Face: https://huggingface.co/diegobit, YouTube (Indiependenti): https://www.youtube.com/@indiependenti"
        }
      ],
      "summary": "Detailed personal and professional information about Diego Giorgini, including his current role as an AI Engineer, location in La Spezia, Italy, education at the University of Pisa, interests in indie videogames, classic literature, and mechanical keyboards, and links to his various social media and professional profiles."
    },
    {
      "url": "https://diegobit.com/posts",
      "tag": "article_written_by_the_user",
      "relevant_contents": [
        {
          "title_or_tag": "Crawling shouldn't be that hard",
          "content": "o3 has a powerful search – it can even keep searching the web for minutes until it finds the precise location where a picture was shot. Maybe my Opinion Search is already outdated... Sometimes all I want is to download the documentation of a website and upload it to Claude or ChatGPT project documents. When I'm about to work on something for a few days where I know the required knowledge is newer than the LLMs' cutoff, I don't want to ask the llm to do a web search at the start of every chat to re-load all the context ..."
        },
        {
          "title_or_tag": "An MCP server for my Aranet4 CO2 sensor",
          "content": "I've been using an Aranet4 CO2 sensor for a couple of years now, and I love it. It's a small device that measures CO2, temperature, humidity, and atmospheric pressure. It's battery-powered and connects via Bluetooth. The problem is that the official app is not very good, and I wanted to integrate it with my home automation system. So I decided to write an MCP server for it."
        },
        {
          "title_or_tag": "The importance of a good prompt",
          "content": "A good prompt is essential for getting good results from an LLM. It's like asking a question to a human: if you ask a vague question, you'll get a vague answer. If you ask a precise question, you'll get a precise answer. This post explores some tips for writing good prompts."
        }
      ],
      "summary": "A collection of blog posts written by Diego Giorgini, covering topics such as web crawling, integrating IoT devices (Aranet4 CO2 sensor), and the importance of good prompts for LLMs."
    },
    {
      "url": "https://diegobit.com/favorites",
      "tag": "other",
      "relevant_contents": [
        {
          "title_or_tag": "Baba is Eval",
          "content": "Brilliant! He had the idea to use Baba is You as an LLM benchmark similar to ARC-AGI. He reversed engineered the game code and made an MCP server to expose the game state. I'm gonna play with it!"
        },
        {
          "title_or_tag": "AGI Is Not Multimodal",
          "content": "Great article. A more rational take on AGI and multimodality compared to the previous link."
        },
        {
          "title_or_tag": "The library came alive",
          "content": "Are LLMs going to be enough, or are embodiment and agency necessary? A poetic view."
        },
        {
          "title_or_tag": "Lily58 and Lotus58 keyboard layouts",
          "content": "I'm enjoying this couple of split keyboards. The link points to the repo with my custom layouts to be used on the Vial app and some explanation of my choices."
        },
        {
          "title_or_tag": "How I use LLMs",
          "content": "If you are not conviced, or you don't understand LLMs, ChatGPT etc, please watch this video. Karpathy has an exceptional ability to explain complex topics in simple non trivial ways. He recently started a series targeted at a general audience that explains all the fundamental building blocks and provides the correct mental models to understand ChatGPT, how it works and how it's trained."
        },
        {
          "title_or_tag": "The Only Unbreakable Law",
          "content": "A hierarchy that creates information silos between teams prevents them from sharing information effectively, forcing each to work around the lack of communication. This constrains the space of possible software designs to those that mirror the organizational structure. When the structure naturally reflects the problem domain, great. But when it doesn't, we're ruling out the best architecture from the start. This video illustrates that perfectly, explaining it through the lens of Conway's Law, with plenty of examples."
        },
        {
          "title_or_tag": "On the measure of Intelligence",
          "content": "Fundamental paper for AI research. Chollet tries to find a definition of intelligence that is not naive, not something that shifts every time there is a new model that beats humans at some narrow task (like chess, at go, or that writes like humans). He aims for a definition that lets us discuss AGI in a practical way, not the holy grail that solves all the problems on earth, but a concrete goal we can actually work toward. Brutally summarized: For Chollet, intelligence is the ability to generalize quickly beyond what is known; in his words: \"skill-acquisition efficiency\"."
        },
        {
          "title_or_tag": "Neural network training makes beautiful fractals",
          "content": "Really fascinating to see fractals here. What makes it so is that this is a real phenomenon, like visualizations that dive deeper and deeper into the world of small-scale physics, not just a mathematical object. It reminds me of the beautiful ending of Fez."
        },
        {
          "title_or_tag": "The Fibonacci Matrix",
          "content": "I love visualization that give a new intuition about something that is hard, solely with algebra, and I love clever algorithmic optimizations. This article has both. This article will also make you wonder why you never new about the clever ways to compute it and why you had to write the Fibonacci sequence in countless unoptimized ways in University."
        }
      ],
      "summary": "A list of Diego Giorgini's favorite links, showcasing his interests in AI research (LLM benchmarks, AGI, intelligence definitions), software development principles (Conway's Law), and personal hobbies like mechanical keyboards and visual phenomena."
    }
  ],
  "overall_summary": "Diego Giorgini is an AI Engineer based in La Spezia, Italy, with an MS in Computer Science from the University of Pisa, specializing in Recurrent Neural Networks. His professional interests include AI development, as evidenced by his role at AI Technologies and his blog posts on topics like LLMs and IoT integration. Personally, he enjoys indie videogames, classic literature, and mechanical keyboards. His 'Favorites' section further highlights his intellectual curiosity in AI theory and practical applications, as well as his appreciation for insightful technical content and unique artistic expressions."
},
"huggingface": {
  "knowledge_cutoff_date": "2025-06-27",
  "name": "Diego Giorgini",
  "username": "diegobit",
  "followers": 0,
  "following": 1,
  "ai_ml_interests": "None yet",
  "recent_activity": [],
  "organizations": "None yet",
  "posts": [],
  "articles": [],
  "collections": [],
  "papers": [],
  "models": [
    {
      "name": "diegobit/Phi-3-mini-4k-instruct-ita-orpo-v2",
      "tag": "Text Generation",
      "size": "2.07B params",
      "updated_date": "May 15, 2024",
      "downloads": 10,
      "hearts": 0,
      "summary": "This is phi-3-mini-4k-instruct ORPO finetuning for the italian language over the Alpaca vs. Alpaca italian dataset: efederici/alpaca-vs-alpaca-orpo-dpo."
    },
    {
      "name": "diegobit/llama-3-8b-Instruct-bnb-4bit-ita-orpo",
      "tag": "Text Generation",
      "size": "4.65B params",
      "updated_date": "Not available for the model (only for the dataset used for training, which was Feb 21, 2024).",
      "downloads": 9,
      "hearts": 0,
      "summary": "This is llama-3-8b ORPO finetuning for the Italian language over the ultrafeedback Italian dataset: mii-community/ultrafeedback-preferences-translated-ita."
    },
    {
      "name": "diegobit/llama-3-8b-ita-4k-orpo-v3",
      "tag": "Text Generation",
      "size": "4.65B params",
      "updated_date": "Information not explicitly available for the model itself. The page provides 'Updated' dates for the datasets used to train the model (May 15, 2024 for efederici/alpaca-vs-alpaca-orpo-dpo and Feb 21, 2024 for mii-community/ultrafeedback-preferences-translated-ita).",
      "downloads": 9,
      "hearts": 0,
      "summary": "This is a llama-3-8b ORPO finetuning for the Italian language. It was trained using a concatenation of two datasets: mii-community/ultrafeedback-preferences-translated-ita and efederici/alpaca-vs-alpaca-orpo-dpo. Key differences from a previous version include using a non-instruct starting model (astronomer/Llama-3-8B-Special-Tokens-Adjusted), no 4-bit loading, and an increased sequence max length of 4096 for finetuning due to higher GPU memory needs."
    }
  ],
  "datasets": [],
  "summary": "Diego Giorgini's Hugging Face profile primarily showcases three AI models, all focused on Text Generation and Transformers, specifically finetuning large language models (Phi-3-mini and Llama-3-8b) for the Italian language. The models are relatively recent, with updates in May 2024, indicating ongoing engagement. The primary language supported is Italian. While the number of downloads is modest (around 10 per model), the consistent focus on Italian language models suggests a dedicated effort in this niche. The projects are all related to finetuning existing models rather than developing new architectures from scratch, which implies a focus on application and refinement rather than foundational research. The 'AI & ML interests' and 'Organizations' sections are empty, suggesting a more individual or less publicly declared collaborative effort. Overall, Diego Giorgini is contributing a small but focused amount of open-source code, primarily in the domain of Italian language model finetuning, demonstrating a consistent effort in this specific area."
},
"x": {
  "knowledge_cutoff_date": "2025-06-27",
  "name": "Diego Giorgini",
  "x_handle": "@diegobit10",
  "bio": "Computer Scientist • Machine Learning • GenAI",
  "website": "diegobit.com",
  "follower_count": "49",
  "following_count": "105",
  "posts": [],
  "repost_and_like_summary": "Diego Giorgini's recent activity (10 reposts) indicates a strong interest in Artificial Intelligence, particularly in Machine Learning, Generative AI, and Language Models. He reposts content related to new AI models (SmolLM3, Kimi K2), advancements in deep learning and optimization (SGD vs AdamW, H-Net for tokenization), and the practical application and implications of AI (Claude Artifacts, LLM pretraining, AI safety papers). He also shows interest in robotics and the open-source community within AI.",
  "profile_summary": "Diego Giorgini is a Computer Scientist specializing in Machine Learning and Generative AI. His X.com profile shows he is actively engaged with the latest developments in the AI field, frequently sharing content related to new models, research, and practical applications of AI."
},
"linkedin": {
  "knowledge_cutoff_date": "2025-06-27",
  "personal_info": {
    "name": "Diego Giorgini",
    "job_title": "Machine Learning Engineer",
    "linkedin_url": "https://www.linkedin.com/in/diego-giorgini",
    "current_work_position": "Machine Learning Engineer",
    "sector": "Artificial Intelligence / Technology",
    "user_bio": "null",
    "location": "Pisa, Italy",
    "email": "null",
    "phone_number": "null",
    "website": "www.linkedin.com/in/diego-giorgini",
    "others": []
  },
  "experience": [
    {
      "job_title": "Machine Learning Engineer",
      "company": "AI Technologies",
      "employment_type": "Full-time",
      "duration_or_dates": "July 2019 - Present (6 years 1 month)",
      "summary": "null"
    },
    {
      "job_title": "Software Developer",
      "company": "AI Technologies",
      "employment_type": "Full-time",
      "duration_or_dates": "May 2018 - June 2019 (1 year 2 months)",
      "summary": "null"
    }
  ],
  "education": [
    {
      "education_title": "Laurea Magistrale",
      "university_or_school_name": "Università di Pisa",
      "course_name": "Informatica",
      "duration_or_dates": "2016 - 2019",
      "activities_and_associations": "Thesis: Incremental pretraining of multi-resolution memory networks.",
      "description": "Grade: 110/110 cum laude."
    },
    {
      "education_title": "Laurea Triennale",
      "university_or_school_name": "Università di Pisa",
      "course_name": "Informatica",
      "duration_or_dates": "2013 - 2016",
      "activities_and_associations": "Thesis: \"Group based content sharing: an analysis of some encryption techniques\".",
      "description": "Grade: 93/110."
    }
  ],
  "certifications": [],
  "skills": [],
  "posts": [],
  "interests": "null",
  "profile_summary": "null"
}"""

agent = Agent(
    'gemini-2.5-flash',
    output_type=Output,
    system_prompt=inspect.cleandoc(f"""
        You are the personal AI assistant of Diego Giorgini. You answer personal questions about Diego Giorgini. 

        You have been given information about Diego Giorgini, some of which are extracted from personal websites or socials. You talk like you know and care for Diego Giorgini. You never explicitly say you have been provided context information.

        Context:
        ```json
        {context}
        ```
    """),
    model_settings=settings
)


def ask_agent(question: str) -> Output:
    return asyncio.run(agent.run(question))

# ---------- STREAMLIT ---------
st.title("beststories.com/diegobit")

user_query = st.text_area(
    "Ask your question about Diego:",
    height=120,
    placeholder="What's diego's current job?",
)

if st.button("Send"):
    if not user_query.strip():
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Thinking..."):
        response = ask_agent(user_query)

    st.subheader("Answer")
    st.write(response.output.answer)
