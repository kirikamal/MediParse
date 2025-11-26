from fastapi import FastAPI, Form, UploadFile, File
import uvicorn
from data_extractor import extract_data
import uuid
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/extract_from_document")
def extract_from_document(
        file_format: str = Form(...),
        file: UploadFile = File(...)):

    contents = file.file.read()
    print(f"Received file of size: {len(contents)} bytes")
    file_path = "../uploads/" + str(uuid.uuid4()) + ".pdf"
    print(f"Saving uploaded file to: {file_path}")

    with open(file_path, "wb") as f:
        f.write(contents)
    # pass

    try:
        data =  extract_data(file_format, file_path)
        print(f"Extracted data: {data}")
    except Exception as e:
        data = { "error": str(e) }

    if os.path.exists(file_path):
        os.remove(file_path)

    return data

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
