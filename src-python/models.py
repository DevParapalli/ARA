from dotenv import load_dotenv
load_dotenv()

import os

from langchain_anthropic import ChatAnthropic

ANTHROPIC_KEY = os.environ.get("ANTHROPIC_KEY")

claude_3_haiku = ChatAnthropic(model_name="claude-3-haiku-20240307", anthropic_api_key=ANTHROPIC_KEY) #type: ignore

from langchain_groq import ChatGroq

GROQ_KEY = os.environ.get("GROQ_KEY")

mixtral_groq = ChatGroq(model="mixtral-8x7b-32768", groq_api_key=GROQ_KEY) #type: ignore

