import fitz


class PDFProcessor:

    def extractText(self, file_path):

        document = fitz.open(file_path)

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        return text