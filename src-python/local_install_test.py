from langchain_community.llms import Ollama
import asyncio

llm = Ollama(model="mistral")

# print(llm.invoke("What are LLMs? How do they work? Context: AI, ML and NLP. Answer in short."))

async def invoke():
    chunks = []
    async for chunk in llm.astream("What are LLMs? How do they work? Context: AI, ML and NLP. Answer in short."):
        chunks.append(chunk)
        print(chunk, end="")


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(invoke())
    loop.close()
    

if __name__ == "__main__":
    main()