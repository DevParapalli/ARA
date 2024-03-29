from langchain_community.chat_models import ChatCohere
from langchain_community.retrievers import CohereRagRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

rag = CohereRagRetriever(
    llm=ChatCohere(client=None, async_client=None, cohere_api_key="Qg0vm03ztzlhiMlbTxLQD9r4YALmOuXVRG9B4hwO")
)


def _pretty_print(docs):
    for doc in docs:
        print(doc.metadata)
        print("\n\n" + doc.page_content)
        print("\n\n" + "-" * 30 + "\n\n")


# _pretty_print(rag.get_relevant_documents("What is cohere ai?"))


template = """
Answer the prompt based only on the following information:
{context}

Prompt: {prompt}
"""

prompt = ChatPromptTemplate.from_template(template)

model = ChatCohere(client=None, async_client=None, cohere_api_key="Qg0vm03ztzlhiMlbTxLQD9r4YALmOuXVRG9B4hwO")
# model = Ollama(model="mistral")

chain = {"context": rag, "prompt": RunnablePassthrough()} | prompt | model | StrOutputParser()

output = chain.invoke("What is LangChain ?")

print(output)
