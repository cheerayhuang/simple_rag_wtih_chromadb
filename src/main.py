import logging

from fastapi import FastAPI, File, Path, UploadFile
from pydantic import BaseModel
from typing import Dict, Optional

from db_mappber import db
from rag import RagChain

from settings import Settings

app = FastAPI()

_rag = RagChain()

logging.basicConfig(
    datefmt=Settings.LOG_DATE_FORMAT,
    level=logging.INFO,
    format=Settings.LOG_FORMAT,
)
_log = logging.getLogger('main')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源，也可以指定具体源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

class QuestionParams(BaseModel):
    input: str
    parameters: Dict = {}
    collection: Optional[str] = Settings.DEFAULT_COLLECTION


@app.post("/collections/langchain/documents")
async def save_text(file: UploadFile = File(...)):

    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Unspported file format.")

    content = await file.read()
    content = content.decode("utf-8")

    db.save_doc(content, file.filename)

    return {"message": "保存成功", "code": 200}


@app.post("/llm")
def ask_question(q: QuestionParams):
    ans_ret = _rag(q)

    if ans_ret['answer'] != '':
        return {
            "message": "提问成功",
            "code": 200,
            "data": ans_ret['answer'],
        }

    return {
        "message": "提问失败",
        "code": 400,
    }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
