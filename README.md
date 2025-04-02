# <span style="color:#3271a5">pdf2json</span>  
<span style="color:white">An Intelligent Docker-Based Pipeline for Document Processing with computer vision and NLP for efficient data management</span>  

## <span style="color:#3271a5">Overview</span>  
<span style="color:white">pdf2json is an automated, intelligent pipeline designed to streamline data management. It leverages computer vision and natural language processing (NLP) to extract, process, and structure information from PDF documents. This tool facilitates efficient handling of text and images, offering an organized, JSON-based output to support several kind of workflows.

---

## <span style="color:#3271a5">Key Features</span>
- **Standard Graphical User Interface (GUI)**

  <span style="color:white">The GUI offers a simple yet efficient interface, allowing users to upload PDFs for processing. It also enables users to specify a destination path where the generated JSON file will be saved.


- **Automated Document Processing**  
  <span style="color:white">This feature extracts and processes text from both PDF documents and images, performing tasks such as text cleaning, summarization, and image extraction. The images are decoded into base64 format, and all extracted data is organized and converted into a standardized JSON format. The resulting JSON file is then saved to the user-specified path.

---

## <span style="color:#3271a5">Project Modules</span>  

### <span style="color:#3271a5">1. api</span>  
- **api.py**  
  <span style="color:white">It defines an asynchronous function, that processes uploaded PDF files. It validates the file format, extracts text and metadata using `process_pdf`, saves the results as a JSON file, and sends the PDF to an external API. Errors are handled with HTTP exceptions, and temporary files are cleaned up after processing. Designed for FastAPI, it integrates into a web service for PDF handling.

### <span style="color:#3271a5">2. backend</span>  
- **pdf_processor.py**  
  <span style="color:white">It processes a PDF file by extracting text and images, combining them into a structured format, and returning the results in a standardized JSON object. It handles both scanned and normal PDFs with appropriate processing methods.

#### <span style="color:#3271a5">2.1 normal_pdfs</span> 
- **text_extractor.py**  
  <span style="color:white">It extracts text from each page of a PDF, segments it into paragraphs, and summarizes each paragraph using parallel processing for efficiency. The results are returned as a structured list of summarized paragraphs for each page.


- **image_extractor.py**  
  <span style="color:white">It extracts images and associated text from a PDF document. It decodes images, converts them to base64 format, and extracts text from the images using OCR. The resulting data is returned as a list of dictionaries, each representing the images and extracted text for a specific page.

#### <span style="color:#3271a5">2.2 scanned_pdfs</span> 

- **cid_pdf.py**

  <span style="color:white">It processes a PDF by converting each page into an image, then extracts and summarizes the text from the images. The images are encoded in base64 format, and the extracted text is cleaned and summarized. The results are returned as a dictionary, with each entry representing a page's image data and corresponding text summary.

#### <span style="color:#3271a5">2.3 imgRelated</span> 
- **base64.py**

  <span style="color:white">It converts a PIL Image object into a Base64-encoded string. It handles the conversion of images in different color modes and returns the encoded string, or an empty string if the conversion fails.


- **decoder.py**

  <span style="color:white">It decodes various image formats from PDF files, handling multiple compression and encoding methods such as JPEG, PNG, TIFF, LZW, and ASCII-based encodings. It supports decoding through filters like /DCTDecode, /FlateDecode, and others, returning the decoded image as a PIL Image object or None if decoding fails.


- **preprocess.py**

  <span style="color:white">It preprocesses an image by converting it to grayscale, enhancing contrast, applying a black & white threshold, and reducing noise with a median filter. It returns the processed PIL.Image object.
  

- **text_from_img.py**

  <span style="color:white">This module performs OCR text extraction from an image using Tesseract with preprocessing (grayscale conversion, contrast enhancement, and noise reduction). It then cleans the output by removing line breaks and handling specific edge cases, returning the extracted text or an empty string if processing fails.

### <span style="color:#3271a5">3. models</span>  
- **base_ocr_model.py**

  <span style="color:white">The method takes a PIL Image as input and returns the extracted text as a string.


- **check_pdf.py**

  <span style="color:white">This function checks whether a PDF document is a scanned (image-based) document or a normal text-based PDF. It attempts to extract text and examines the presence of CID fonts, which are typically used in scanned PDFs. If text extraction is not possible or if CID fonts are detected, the function returns True; otherwise, it returns False.
 

- **gpt4_cleaning_text.py**

  <span style="color:white">It utilizes the GPT-4 model via OpenAI's API to clean and enhance the readability of input text. It removes unnecessary whitespace, corrects typos, and improves clarity while preserving the original meaning. In case of an error, the original text is returned.


- **gpt4_summary.py**

  <span style="color:white">It summarizes the input text using the GPT-4 model via OpenAI's API. It first detects the language of the text and generates an appropriate prompt in either English or German, then returns the summarized version. If the language is not supported, it defaults to English. The summary is generated with a maximum token limit of 150 for concise output.


- **nlp_paragraph_detection.py**

  <span style="color:white">This function segments input text into coherent paragraphs using the TextRank algorithm for summarization. It supports both English and German text, dynamically adjusting the number of key sentences per paragraph based on the total length of the text. The resulting paragraphs are returned as a list of strings.


- **tesseract_ocr_model.py**

  <span style="color:white">This is a ready-to-use OCR processor built as an extension of BaseOcrModel, offering standardized text extraction for both English and German content. Using Tesseract's advanced LSTM engine (OEM 3) with automatic layout detection (PSM 3), it delivers accurate results for documents, forms, and structured text layouts while providing clear error messages. The implementation requires minimal preprocessing and returns clean extracted text as plain strings, making it ideal for multilingual document processing pipelines.


### <span style="color:#3271a5">4. tests</span>  
<span style="color:white">The `tests` folder contains automated test cases and scripts designed to validate the functionality, reliability, and performance of the application. It includes unit tests, integration tests, and end-to-end tests for various components, such as the PDF processing logic, OCR functionality, and AI models. By running these tests, we can ensure the code behaves as expected, catch bugs early, and maintain high-quality standards throughout the development process.

---

## <span style="color:#3271a5">Setup and Installation</span>  

### <span style="color:#3271a5">1. Prerequisites</span>  
<span style="color:white">Ensure you have the following installed on your system:
- **Python 3.8 or higher** (recommended: Python 3.10): [Python's official website](https://www.python.org/)
- **Docker** (with Docker Compose, if applicable): [Docker's official website](https://www.docker.com/)
  - On Linux, you may need to install Docker Compose separately
- **Git**: [Git's official website](https://git-scm.com/)
- **Tesseract OCR** (for OCR functionality)
  - On Ubuntu/Debian:
    ```bash
    sudo apt update && sudo apt install -y tesseract-ocr libtesseract-dev
    ```
  - On macOS (using Homebrew):
    ```bash
    brew install tesseract
    ```
  - On Windows:
    - Download installer from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
    - Or using Chocolatey: `choco install tesseract`

### <span style="color:#3271a5">2. Clone the Repository</span>  
<span style="color:white">Clone the project repository to your local machine:

        git clone https://github.com/zohrehasadi00/pdf2json.git
        cd pdf2json

### <span style="color:#3271a5">3. Docker </span>
- Run the Application
  ```bash
  docker build -t myapp . 
  docker run -d -p 8000:8000 --name myapp_container myapp
  ```
- Access the app at: http://localhost:8000
- stop the Container:
  ```bash
  docker stop myapp_container
  ```
