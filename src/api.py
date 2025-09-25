from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Annotated
from pydantic import BaseModel, Field
from main import query

app = FastAPI(title="Query API", description="API to answer user questions", version="1.0.0")

class UserInput(BaseModel):
    question: Annotated[str, Field(..., description="Question input'd by user.")]

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/query")
def answer_query(data: UserInput):
    try:
        answer = query(data.question)
        return JSONResponse(status_code=200, content={"Output": answer})
    except Exception as e:
        return JSONResponse(status_code=500, content={"Error": str(e)})
