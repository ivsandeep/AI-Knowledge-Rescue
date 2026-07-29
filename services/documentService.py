import os
from database.database import SessionLocal
from database.models import Document
from pathlib import Path
from processors.pdfProcessor import PDFProcessor
from processors.docxProcessor import DocxProcessor
from processors.excelProcessor import ExcelProcessor
from pathlib import Path

class DocumentService:

    UPLOAD_FOLDER = "uploads"

    def __init__(self):

        self.pdfProcessor = PDFProcessor()

        self.docxProcessor = DocxProcessor()

        self.excelProcessor = ExcelProcessor()

    async def process_document(self, file):

        os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)

        file_path = os.path.join(
            self.UPLOAD_FOLDER,
            file.filename
        )

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        extension = Path(file.filename).suffix.lower()

        if extension == ".pdf":

            text = self.pdfProcessor.extractText(filePath)

        elif extension == ".docx":

            text = self.docxProcessor.extractText(filePath)

        elif extension in [".xlsx", ".xls"]:

            text = self.excelProcessor.extractText(filePath)

        else:

            raise Exception(f"Unsupported File Type : {extension}")

        db = SessionLocal()

        document = Document(
            fileName=file.filename,
            fileType=Path(file.filename).suffix.lower(),
            filePath=file_path,
            extractedText=text,
            summary=""
        )

        db.add(document)

        db.commit()

        db.close()


        return {
        "fileName": file.filename,
        "fileType": extension,
        "textLength": len(text)
}


