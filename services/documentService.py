import os
from pathlib import Path

from database.database import SessionLocal
from database.models import Document

from processors.pdfProcessor import PDFProcessor
from processors.docxProcessor import DocxProcessor
from processors.excelProcessor import ExcelProcessor


class DocumentService:

    UPLOAD_FOLDER = "uploads"

    def __init__(self):

        self.pdfProcessor = PDFProcessor()
        self.docxProcessor = DocxProcessor()
        self.excelProcessor = ExcelProcessor()

    def _processFile(self, fileName, filePath):

        extension = Path(fileName).suffix.lower()

        if extension == ".pdf":

            text = self.pdfProcessor.extractText(filePath)

        elif extension == ".docx":

            text = self.docxProcessor.extractText(filePath)

        elif extension in [".xlsx", ".xls"]:

            text = self.excelProcessor.extractText(filePath)

        else:

            raise Exception(f"Unsupported File Type: {extension}")

        db = SessionLocal()

        try:

            document = Document(
                fileName=fileName,
                fileType=extension,
                filePath=filePath,
                extractedText=text,
                summary=""
            )

            db.add(document)
            db.commit()

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()

        return {
            "fileName": fileName,
            "fileType": extension,
            "textLength": len(text)
        }

    async def process_document(self, file):

        os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)

        filePath = os.path.join(
            self.UPLOAD_FOLDER,
            file.filename
        )

        with open(filePath, "wb") as buffer:

            buffer.write(await file.read())

        return self._processFile(file.filename, filePath)

    async def process_document_from_path(self, fileName, fileBytes):

        os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)

        filePath = os.path.join(
            self.UPLOAD_FOLDER,
            fileName
        )

        with open(filePath, "wb") as buffer:

            buffer.write(fileBytes)

        return self._processFile(fileName, filePath)