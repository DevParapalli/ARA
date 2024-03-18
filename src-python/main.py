from norag import chain as norag_chain
from rag import chain as rag_chain

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from langserve import add_routes

app = FastAPI(
    title="LLM Runner",
    version="0.0.3"
)

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
    uvicorn.run(app, host="0.0.0.0", port=4945, timeout_keep_alive=3600)