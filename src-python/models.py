from dotenv import load_dotenv
load_dotenv()

import os

from langchain_anthropic import ChatAnthropic

ANTHROPIC_KEY = os.environ.get("ANTHROPIC_KEY")

claude_3_haiku = ChatAnthropic(temperature=0, model_name="claude-3-haiku-20240307", anthropic_api_key=ANTHROPIC_KEY) #type: ignore

from langchain_groq import ChatGroq

GROQ_KEY = os.environ.get("GROQ_KEY")

mixtral_groq = ChatGroq(temperature=0, model="mixtral-8x7b-32768", groq_api_key=GROQ_KEY) #type: ignore

from langchain_community.llms.cohere import Cohere
from langchain_community.chat_models import ChatCohere

COHERE_KEY = os.environ.get("COHERE_KEY")

command_r_cohere = Cohere(cohere_api_key=COHERE_KEY) #type: ignore
chat_command_r_cohere = ChatCohere(model="command-r", cohere_api_key=COHERE_KEY) #type: ignore
chat_cohere = ChatCohere(cohere_api_key=COHERE_KEY) #type: ignore