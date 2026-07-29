from docx import Document


class DocxProcessor:

    def extractText(self, filePath):

        document = Document(filePath)

        extractedText = ""

        for paragraph in document.paragraphs:
            extractedText += paragraph.text + "\n"

        return extractedText