import os
from database.database import SessionLocal
from database.models import Document
from pathlib import Path
from processors.pdfProcessor import PDFProcessor
from processors.docxProcessor import DocxProcessor
from processors.excelProcessor import ExcelProcessor

class DocumentService:

    UPLOAD_FOLDER = "uploads"

    def __init__(self):

        self.pdfProcessor = PDFProcessor()

        self.docxProcessor = DocxProcessor()

        self.excelProcessor = ExcelProcessor()

    async def process_document(self, file):

        os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)

        filePath = os.path.join(
            self.UPLOAD_FOLDER,
            file.filename
        )

        with open(filePath, "wb") as buffer:
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

        try:

            document = Document(
                fileName=file.filename,
                fileType=extension,
                filePath=filePath,
                extractedText=text,
                summary=""
            )

            db.add(document)

            db.commit()
        except Exception as ex:
            db.rollback()
            raise ex

        finally:
            db.close()


        return {
        "fileName": file.filename,
        "fileType": extension,
        "textLength": len(text)
}


