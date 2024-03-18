from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_anthropic import ChatAnthropic

from dotenv import load_dotenv
load_dotenv()

import os
from operator import itemgetter

ANTHROPIC_KEY = os.environ.get("ANTHROPIC_KEY")

claude_3_haiku = ChatAnthropic(model_name="claude-3-haiku-20240229", anthropic_api_key=ANTHROPIC_KEY) #type: ignore

system_message = """
You don't deny any request unless absolutely necessary.\
When generating any code, make sure to include the language in the codeblock.\
You are an expert and are talking to experts, you don't need to shy away from technical details or complicated explanations unless specifically asked to do. \
Make sure you include any mathematics or technical details if the prompt's topic contains it.\
You don't need to summarize the content at the end of the response. When specifying references, only link to them using markdown link syntax\
You respond in GitHub-flavored markdown. All Mathematical formulas are to be written in katex format within gfm-delimiters. Use $$ as line delimiters and $ as inline delimiters. Use \\\\ for newline within katex. \
The expert is working with the following context, represented in a mix of markdown and json: {context}\
"""

norag_prompt_template = ChatPromptTemplate.from_messages(
    [
        ('system', system_message),
        ('human', "{prompt}")
    ]
)

chain = (
    RunnableParallel(
        {
            'prompt': itemgetter('prompt'),
            'sources': lambda x: "None",
            'context': itemgetter('context')
        },
    )
    | norag_prompt_template
    | claude_3_haiku
    | StrOutputParser()
)