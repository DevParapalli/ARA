from rag import chain

k = chain.stream({"prompt": "Explain Retrieval Augmented Generation", "context": "None"})

for chunk in k:
    print(chunk.dict())
