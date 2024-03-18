from operator import itemgetter
from langchain_core.runnables import (
    RunnableParallel, 
    RunnablePassthrough
)

from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_community.retrievers import (
    WikipediaRetriever,
    CohereRagRetriever
)

from langchain.retrievers.document_compressors import (
    CohereRerank
)

from langchain.retrievers import (
    ContextualCompressionRetriever,
    MergerRetriever,
)

from langchain_core.output_parsers import (
    StrOutputParser
)

from langchain_core.retrievers import (
    BaseRetriever
)

from langchain_core.callbacks import  (
    CallbackManagerForRetrieverRun
)

from langchain_core.documents import (
    Document
)

from langchain_community.chat_models import (
    ChatCohere
)
from langchain_anthropic import ChatAnthropic

from langchain_groq import ChatGroq


from dotenv import load_dotenv
load_dotenv()

import os

GROQ_KEY = os.environ.get("GROQ_KEY")
COHERE_KEY = os.environ.get("COHERE_KEY")
ANTHROPIC_KEY = os.environ.get('ANTHROPIC_KEY')


mixtral = ChatGroq(temperature=.5, model="mixtral-8x7b-32768", groq_api_key=GROQ_KEY) #type: ignore
claude_3_haiku = ChatAnthropic(model_name="claude-3-haiku-20240229", anthropic_api_key=ANTHROPIC_KEY) #type: ignore

cohere_rag = CohereRagRetriever(
    llm = ChatCohere(
            client=None,
            async_client=None,
            cohere_api_key=COHERE_KEY
            )
)

wikipedia_rag = WikipediaRetriever(
    wiki_client=None, 
    top_k_results=2
)

lotr = MergerRetriever(
    retrievers=[
        cohere_rag,
        wikipedia_rag,
    ]
)

compressor = CohereRerank(
    cohere_api_key=COHERE_KEY
)

compression_retriever = ContextualCompressionRetriever(
    base_retriever=lotr,
    base_compressor=compressor
)

compression_retriever_chain = (
    itemgetter('prompt')
    | compression_retriever
)

class ContextRetriever(BaseRetriever):
    """ This is supposed to be a retriever that returns the notebook cells for a given notebook id using supabase"""
    
    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun) -> list[Document]:
        return [
            Document(page_content="Custom Document")
        ]

context_rag = ContextRetriever()

context_rag_chain = (
    itemgetter('context')
    | context_rag
)


def format_docs(docs: list[Document]):
    return "<documents>" + "\n".join(
f"""<document>
<id>{doc.metadata.get('id', "--")}</id>
<title>{doc.metadata.get('title', "--")}</title>
<document_content>{doc.page_content}</document_content>
</document>""" 
for doc in docs
    ) + "</documents>"

def get_formatted_docs_from_chain(input):
    return format_docs(input["sources"])


system_message = """
You don't deny any request unless absolutely necessary.\
When generating any code, make sure to include the language in the codeblock.\
You are an expert and are talking to experts, you don't need to shy away from technical details or complicated explanations unless specifically asked to do. \
Make sure you include any mathematics or technical details if the prompt's topic contains it.\
You don't need to summarize the content at the end of the response. When specifying references, only link to them using markdown link syntax\
You respond in GitHub-flavored markdown. All Mathematical formulas are to be written in katex format within gfm-delimiters. Use $$ as line delimiters and $ as inline delimiters. Use \\\\ for newline within katex. \
The expert is working with the following context, represented in an unstructured manner: {context}\
You can use the following information to complete the user's prompts if you need it, you can still answer the question without using these: {sources}
"""


answer_prompt_template = ChatPromptTemplate.from_messages(
    [
        ('system', system_message),
        ('human', "{prompt}")
    ]
)

answer_chain = (
    RunnableParallel(
        {
            'prompt': itemgetter('prompt'),
            'sources': get_formatted_docs_from_chain,
            # 'context': context_rag_chain
            'context': itemgetter('context')
        },
    )
    | answer_prompt_template
    | claude_3_haiku
    | StrOutputParser()
)


chain = (
    RunnableParallel(
        {
            'prompt': itemgetter('prompt'),
            'sources': compression_retriever_chain,
            'context': context_rag_chain
        },
    )
    | RunnablePassthrough.assign(response=answer_chain).with_config(run_name="add_response")
)

