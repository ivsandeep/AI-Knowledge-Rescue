from fastapi import FastAPI, UploadFile, File
from services.documentService import DocumentService
import os
app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "AI Knowledge Rescue Agent is running"
    }




service = DocumentService()
@app.post("/process-document")
async def process_document(file: UploadFile = File(...)):

    extracted_text = await service.process_document(file)

    result = await documentService.process_document(file)

    return {
        "status": "SUCCESS",
        "message": "Document processed successfully",
        "fileName": result["fileName"],
        "fileType": result["fileType"],
        "textLength": result["textLength"]
    }