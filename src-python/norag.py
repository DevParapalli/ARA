from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser

from operator import itemgetter

from models import claude_3_haiku,mixtral_groq

system_message = """
You are ARA, a intelligent research assistant created by Team ARA of Government College of Engineering, Nagpur.
You don't deny any request unless absolutely necessary.
When generating any code, make sure to include the language in the codeblock.
You are an expert and are talking to experts, you don't need to shy away from technical details or complicated explanations unless specifically asked to do. 
Make sure you include any mathematics or technical details if the prompt's topic contains it.
You don't need to summarize the content at the end of the response. When specifying references, only link to them using markdown link syntax
You respond in GitHub-flavored markdown. All Mathematical formulas are to be written in katex format within gfm-delimiters. Use $$ as line delimiters and $ as inline delimiters. Use \\\\ for newline within katex. 

Additional working information from the user: 
<documents>
{context}
</documents>
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
    # | claude_3_haiku
    | mixtral_groq
    | StrOutputParser()
)