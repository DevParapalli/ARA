import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from norag import chain as norag_chain
from rag import chain as rag_chain

load_dotenv()

app = FastAPI(title="LLM Runner", version="0.0.3")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:5173", "http://localhost:4173", "https://ara.parapalli.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_routes(app, norag_chain, path="/norag")
add_routes(app, rag_chain, path="/rag")


@app.get("/")
async def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn
    import sys
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    PORT = int(os.getenv("PORT", 4945))
    uvicorn.run(app, host="0.0.0.0", port=PORT, timeout_keep_alive=3600)
