from operator import itemgetter
from langchain_community.retrievers import (
    CohereRagRetriever, 
    ArxivRetriever, 
    PubMedRetriever, 
    WikipediaRetriever
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from typing import TypedDict
from langchain_core.runnables import (
    RunnableParallel, 
    RunnablePassthrough
)
from langchain_community.chat_models import ChatCohere

from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()
import os

from langserve import add_routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

GROQ_KEY = os.environ.get("GROQ_KEY")
COHERE_KEY = os.environ.get("COHERE_KEY")


rag = CohereRagRetriever(llm=ChatCohere(client=None, async_client=None, cohere_api_key=COHERE_KEY))
chat = ChatGroq(temperature=0.25, model="mixtral-8x7b-32768", groq_api_key=GROQ_KEY)

# arxiv_retriever = ArxivRetriever(top_k_results=5).with_config(run_name="arxiv")

wiki_retriver = WikipediaRetriever(top_k_results=5).with_config(run_name="wikipedia")

system_message = """
You don't deny any request unless absolutely necessary.\
When generating any code, make sure to include the language in the codeblock.\
You are an expert and are talking to experts, you don't need to shy away from technical details or complicated explanations unless specifically asked to do. \
Make sure you include any mathematics or technical details if the prompt's topic contains it.\
You don't need to summarize the content at the end of the response.\
The expert is working with the following context, represented in a mix of markdown and json: {context}\
You can use the following information to complete the user's prompts if you need it, these are your sources (refer to them in the response as my sources): {sources}
"""

# TODO: Add user's context (provided by user and in db) to the prompt.

prompt_template = ChatPromptTemplate.from_messages(
    [
        ('system', system_message),
        ('human', "{prompt}")
    ]
)

def fuse_docs(input):
    results_map = input["sources"]
    names, docs = zip(
        *((name, doc) for name, docs in results_map.items() for doc in docs)
    )
    return list(zip(names, docs)) 

def format_named_docs(named_docs):
    return "\n\n".join(
        f"Source: {source}\n\n{doc.page_content}" for source, doc in named_docs
    )

def merge(x):
    return x['context'] + '\n\nPrompt:' +  x['prompt']


retrieve_all = merge | RunnableParallel(
    {
        'rag': rag, 
        # 'wikipedia': wiki_retriver
    }
).with_config(run_name="retrieve_all")

class Prompt(TypedDict):
    prompt: str
    context: str


answer_chain = (
    {
    "prompt": itemgetter("prompt"),
    "sources": lambda x: format_named_docs(x["sources"]),
    "context": itemgetter("context"),
}
| prompt_template
| chat
| StrOutputParser()
).with_config(run_name="answer_chain")

chain = (
    (
        RunnableParallel(
            {"prompt": itemgetter("prompt") or "", "sources": retrieve_all, "context":itemgetter("context") or "None"}
        ).with_config(run_name="add_sources")
        | RunnablePassthrough.assign(sources=fuse_docs).with_config(
            run_name="fuse_docs"
        )
        | RunnablePassthrough.assign(response=answer_chain).with_config(
            run_name="add_response"
        )
    )
    .with_config(run_name="chain")
)

app = FastAPI(
    title="mixtral_groq_cohere-rag",
    description="mixtral_groq_cohere-rag",
    version="0.0.2",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:5173", "http://localhost:4173", "https://ara.parapalli.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_routes(app, chain, path="/rag")

norag_answer_chain = (
    {
    "prompt": itemgetter("prompt"),
    "sources": lambda x: "None", # lambda x: format_named_docs(x["sources"]),
    "context": itemgetter("context"),
}
| prompt_template
| chat
| StrOutputParser()
).with_config(run_name="answer_chain")

norag_chain = (
    RunnablePassthrough.assign(response=norag_answer_chain).with_config(
        run_name="add_response"
    ) 
)

add_routes(app, norag_chain, path="/norag")

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4945)
