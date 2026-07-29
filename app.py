from fastapi import FastAPI, UploadFile, File
from services.documentService import DocumentService
import os
from database.initDb import initDb

app = FastAPI()

initDb()

from fastapi import FastAPI
import os

@app.get("/debug/uploads")
def debugUploads():
    uploadDir = "uploads"

    if not os.path.exists(uploadDir):
        return {
            "exists": False,
            "currentDirectory": os.getcwd()
        }

    return {
        "exists": True,
        "currentDirectory": os.getcwd(),
        "files": os.listdir(uploadDir)
    }

@app.get("/")
def home():
    return {
        "message": "AI Knowledge Rescue Agent is running"
    }




service = DocumentService()

@app.post("/process-document")
async def process_document(file: UploadFile = File(...)):

    result = await service.process_document(file)

    return {
        "status": "SUCCESS",
        "message": "Document processed successfully",
        "fileName": result["fileName"],
        "fileType": result["fileType"],
        "textLength": result["textLength"]
    }