from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing_extensions import Doc
import traceback

def fun(query):
  chat_history = []
  result = chain({"question":query, "chat_history": chat_history})
  chat_history = [(query, result["answer"])]
  return result['answer']

origins = ["*"]
app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins = origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

class RAG_user(BaseModel):
  query: str


@app.post("/RAG_api")
async def RAG_llm_model(reqPayload: RAG_user):
  try:
    payload = reqPayload.dict()
    query = payload["query"]

    resp = {
        "status_code": 200,
        "error_msg": {},
        "response": {}
    }

    result = fun(query)
    
    if result:
      resp['status_code'] = 200
      resp['response'] = result
    
    return resp
  
  except:
    resp['status_code'] = 400
    resp['error_msg'] = str(traceback.format_exec())
  
  return resp
