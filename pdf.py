import PyPDF2


def readPdf(filePath):
    with open(filePath, 'rb') as pdfObj:
        pdfReader = PyPDF2.PdfReader(pdfObj)
        text = ""
        for page in pdfReader.pages:
            text += page.extract_text()
    return text

