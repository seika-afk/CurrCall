from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Annotated
from pydantic import BaseModel, Field
import asyncio
import logging

app = FastAPI(title="Query API", description="API to answer user questions", version="1.0.0")

_query_function = None
_loading_lock = asyncio.Lock()

class UserInput(BaseModel):
    question: Annotated[str, Field(..., description="Question input'd by user.")]

async def get_query_function():
    """Lazy load the query function and its dependencies"""
    global _query_function, _loading_lock
    
    if _query_function is not None:
        return _query_function
    
    async with _loading_lock:
        # Double-check pattern
        if _query_function is not None:
            return _query_function
        
        try:
            # Import heavy dependencies only when needed
            from main import query
            _query_function = query
            logging.info("Query function loaded successfully")
            return _query_function
        except Exception as e:
            logging.error(f"Failed to load query function: {e}")
            raise e

@app.get("/")
def root():
    return {"status": "ok", "message": "FastAPI server is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/query")
async def answer_query(data: UserInput):
    try:
    
        query_func = await get_query_function()
      
        loop = asyncio.get_event_loop()
        answer = await loop.run_in_executor(None, query_func, data.question)
        
        return JSONResponse(status_code=200, content={"Output": answer})
    except Exception as e:
        logging.error(f"Error in answer_query: {e}")
        return JSONResponse(status_code=500, content={"Error": str(e)})
