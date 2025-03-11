# <span style="color:#3271a5">MediLink</span>  
<span style="color:white">An Intelligent Pipeline for Medical Document Processing</span>  

## <span style="color:#3271a5">Overview</span>  
<span style="color:white">MediLink is an automated, intelligent pipeline designed to streamline medical data management. It leverages computer vision and natural language processing (NLP) to extract, process, and structure information from PDF medical documents. This tool facilitates efficient handling of text and images, offering an organized, JSON-based output to support healthcare workflows.

---

## <span style="color:#3271a5">Key Features</span>  
- **Automated Document Processing**  
  <span style="color:white">Extracts text and images from PDF medical documents and converts them into a structured, standardized format.  

- **Image-Text Association**  
  <span style="color:white">Associates extracted images with relevant text paragraphs or sections and stores the linked data in a JSON file for seamless integration.   

---

## <span style="color:#3271a5">Project Modules</span>  

### <span style="color:#3271a5">1. api</span>  
- **api.py**  
  <span style="color:white">It defines an asynchronous function, `extract_text_from_pdf`, that processes uploaded PDF files. It validates the file format, extracts text and metadata using `process_pdf`, saves the results as a JSON file, and sends the PDF to an external API. Errors are handled with HTTP exceptions, and temporary files are cleaned up after processing. Designed for FastAPI, it integrates into a web service for PDF handling.

### <span style="color:#3271a5">2. backend</span>  
- **pdf_processor.py**  
  <span style="color:white">It processes a PDF file by extracting both text and images. It uses `pdfplumber` to extract text and metadata from each page, and a `PdfImageTextExtractor` to extract and process images. The extracted text and image data are combined into a structured format, including paragraphs, image descriptions, and related text. The function `process_pdf` handles the entire process, returning a dictionary with the combined data or an error message if processing fails. Designed for efficiency, it integrates text and image extraction into a single workflow for comprehensive PDF analysis.


- **text_extractor.py**  
  <span style="color:white">It extracts and summarizes text from a PDF page. It identifies sections and paragraphs, processes them using a `summarize_text` function (powered by GPT-4), and organizes the results into structured data. Sections with titles are summarized individually, while standalone paragraphs are summarized separately. Errors during summarization are handled gracefully, ensuring the function returns meaningful output even if issues arise. Designed for efficiency, it provides a clean and organized summary of the page's content.


- **image_extractor.py**  
  It defines a `PdfImageTextExtractor` class that extracts and processes images from PDF files. It decodes images embedded in PDFs, converts them to Base64, and uses OCR (via `TesseractOcrModel`) to extract text from the images. Additionally, it generates image descriptions using the BLIP model and links extracted text to relevant paragraphs in the document. The class organizes the results into a structured format, including Base64-encoded images, descriptions, extracted text, and related paragraphs. Designed for efficiency, it integrates image and text processing into a cohesive workflow for comprehensive PDF analysis.

### <span style="color:#3271a5">3. models</span>  
<span style="color:white">It contains the core AI and machine learning models used in the application, including `base_ocr.py` for defining the OCR interface, `blip.py` for generating image captions using the BLIP model, `gpt4.py` for advanced text summarization with GPT-4, and `tesseract_ocr.py` for implementing the Tesseract OCR engine. These models work together to enable text extraction, image understanding, and summarization, forming the foundation of the application's AI capabilities.

### <span style="color:#3271a5">4. tests</span>  
<span style="color:white">The `tests` folder contains automated test cases and scripts designed to validate the functionality, reliability, and performance of the application. It includes unit tests, integration tests, and end-to-end tests for various components, such as the PDF processing logic, OCR functionality, and AI models. By running these tests, we can ensure the code behaves as expected, catch bugs early, and maintain high-quality standards throughout the development process.

---

## <span style="color:#3271a5">Setup and Installation</span>  

### <span style="color:#3271a5">1. Prerequisites</span>  
<span style="color:white">Ensure you have the following installed on your system:
- **Python 3.8 or higher** (recommended: Python 3.10): [Python's official website](https://www.python.org/)
- **Docker** (with Docker Compose, if applicable): [Docker's official website](https://www.docker.com/)
- **Git**: [Git's official website](https://github.com/login)
- **Tesseract OCR** (for OCR functionality)
  - On Ubuntu/Debian:
    ```bash
    sudo apt update
    sudo apt install tesseract-ocr
    ```
  - On macOS (using Homebrew):
    ```bash
    brew install tesseract
    ```
  - On Windows:
    - Download the installer from [Tesseract GitHub](https://github.com/tesseract-ocr/tesseract) and add it to your system PATH.

### <span style="color:#3271a5">2. Clone the Repository and Set Up Environment Variables</span>  
<span style="color:white">Clone the project repository to your local machine:
  ```bash
  git clone https://github.com/your-username/your-repo.git
  cd your-repo

Create a .env file and add necessary environment variables
echo "OPENAI_API_KEY=your_openai_api_key" > .env
echo "BLIP_MODEL_PATH=path_to_blip_model" >> .env
echo "TESSERACT_PATH=/usr/bin/tesseract" >> .env 

### <span style="color:#3271a5">4. Build and Run the Docker Container</span>
1. Build the Docker image:
    ´´´bash
    docker build -t your-app-name .
2. Run the Docker container:
 ´´´bash
 docker run -p 8000:8000 your-app-name


# 28A745: green
# 007BFF : blue
# 6F42C1 :light purple
# FD7E14 :orange
# 20C997 : teal: light green
#DC3545 :red
#FFC107 :gold
#FF6F61:coral
6610F2:dark purple , indigo
