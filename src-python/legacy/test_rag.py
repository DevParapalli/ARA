from rag import chain
from langchain_core.messages import HumanMessage

k = chain.stream({'prompt': "Explain Retrieval Augmented Generation", 'context': 'None'})

for chunk in k:
    print(chunk.dict())



