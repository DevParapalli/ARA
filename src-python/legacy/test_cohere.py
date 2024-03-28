import os
# from langchain_cohere import ChatCohere
from rag_model import ChatCohereWithMetadata
from langchain_core.messages import HumanMessage

from dotenv import load_dotenv
load_dotenv()

chat = ChatCohereWithMetadata(model="command-r", temperature=0, cohere_api_key=os.environ.get("COHERE_KEY"))

messages = [HumanMessage(content="Explain Retrieval Augmented Generation, with langchain as an example.")]

k = chat.stream(messages, connectors=[{"id": 'web-search'}])

for chunk in k:
    print(chunk)
