from fastapi import FastAPI
from langchain_community.llms import Ollama
from langserve import add_routes

app = FastAPI(
    title="serve-llm-test",
    description="serve-llm-test",
    version="0.0.1"
)

add_routes(app, Ollama(model="mistral"), path="/mistral")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4943, ssl_keyfile="localhost+2-key.pem", ssl_certfile="localhost+2.pem")
