import os

from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langserve import add_routes

load_dotenv()


GROQ_KEY = os.environ.get("GROQ_KEY")

mixtral = ChatGroq(temperature=-0.5, model="mixtral-8x7b-32768", groq_api_key=GROQ_KEY)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You don't deny any request unless absolutely necessary.\
When generating any code, make sure to include the language in the codeblock.\
You are an expert and are talking to experts, you don't need to shy away from technical details or complicated explanations unless specifically asked to do. \
Make sure you include any mathematics or technical details if the prompt's topic contains it.\
You don't need to summarize the content at the end of the response. When specifying references, only link to them using markdown link syntax\
You respond in GitHub-flavored markdown. All Mathematical formulas are to be written in katex format within gfm-delimiters. Use $$ as line delimiters and $ as inline delimiters. Use \\\\ for newline within katex. \
""",
        ),
        ("human", "{prompt}"),
    ]
)

chain = prompt | mixtral

app = FastAPI()

add_routes(app, chain, path="/norag")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=4945)
