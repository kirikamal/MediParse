from pdf2image import convert_from_path
import pytesseract
from . import util
from .parser_patient_details import ParserPatientDetails
from .parser_prescription import ParserPrescription

def extract_data(file_format, file_path):
    # Extracting text from pdf file
    POPPLER_PATH = "/opt/homebrew/bin"
    pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

    pages = convert_from_path(file_path, poppler_path=POPPLER_PATH)
    document_text = ''

    if len(pages) > 0:
        page = pages[0]
        processed_image = util.preprocess_image(page)
        text = pytesseract.image_to_string(processed_image, lang='eng')
        document_text = '\n' + text
        print(f"document_text: {document_text}")

    # Extract fields from text
    if file_format == 'prescription':
        extracted_data = ParserPrescription(document_text).parse()
    elif file_format == 'patient_details':
        extracted_data = ParserPatientDetails(document_text).parse()
    else:
        raise Exception(f"Invalid document format: {file_format}")

    return extracted_data


if __name__ == '__main__':
    data = extract_data('prescription', '../sample_docs/prescription1.pdf', )
    print(data)
