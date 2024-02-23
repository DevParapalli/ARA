from langchain_community.retrievers import CohereRagRetriever
from langchain_community.chat_models import ChatCohere
from langchain_community.llms import Ollama, Cohere
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langserve import add_routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mistletoe
from mistletoe.block_token import CodeFence
import json
import os

import dotenv
dotenv.load_dotenv()
# import mangum

COHERE_KEY = os.environ.get("COHERE_KEY")

rag = CohereRagRetriever(llm=ChatCohere(client = None, async_client= None, cohere_api_key=COHERE_KEY))
# code_rag = CohereRagRetriever(llm=Cohere(client = None, async_client= None, cohere_api_key=COHERE_KEY))


normal_template = """
Here is some additional context you may require to work with the prompt:
{context}

Prompt: {prompt}
"""

chat_prompt = ChatPromptTemplate.from_template(normal_template)
# code_prompt = ChatPromptTemplate.from_template(code_template)
code_prompt = ChatPromptTemplate.from_messages(
    [
        ('system', "You only output code and nothing else. You include comments in code only when necessary. Only generate code, do not use any markdown symbols, and do not include the prompt.Make sure the code can be run and provide comments only if necessary. The code should be very readable and should be free of any errors.Use the following to generate the code according to the prompt:{context}"),
        ('user', "{prompt}")
    ]
)

chat_model = ChatCohere(client = None, async_client= None, cohere_api_key=COHERE_KEY)
# model = Ollama(model="mistral")
code_model = Cohere(client = None, async_client= None, cohere_api_key=COHERE_KEY)

chat_chain = (
    {"context": rag, "prompt":RunnablePassthrough()}
    | chat_prompt
    | chat_model
    | StrOutputParser()
)

def _sanitize_output(text: str):
    doc = mistletoe.Document(text)
    for token in doc.children:
        if isinstance(token, CodeFence):
            yield {'language': token.language, 'code': token.content}

def get_code_from_text(text: str):
    return json.dumps(list(_sanitize_output(text)))

code_chain = (
    {"context": rag, "prompt":RunnablePassthrough()}
    | code_prompt
    | code_model
    | StrOutputParser()
    # | get_code_from_text
)

# output = chain.invoke("What is LangChain ?")
# print(output)

app = FastAPI(
    title="serve-rag-chain-test",
    description="serve-rag-chain-test",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:5173", "http://localhost:4173", "https://ara.parapalli.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_routes(app, chat_chain, path="/chat")
add_routes(app, code_chain, path="/code")

@app.get("/")
def read_root():
    return {"Hello": "World"}


# handler = mangum.Mangum(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4945)


