# <span style="color:#3271a5">pdf2json</span>  
<span style="color:white">An Intelligent Docker-Based Pipeline for Document Processing with OCR and NLP for efficient data management</span>  

## <span style="color:#3271a5">Overview</span>  
<span style="color:white">pdf2json is an automated, intelligent pipeline designed to streamline data management. It leverages Optical Character Recognition (OCR) and natural language processing (NLP) to extract, process, and structure information from PDF documents. This tool facilitates efficient handling of text and images, offering an organized, JSON-based output to support several kind of workflows.

---

## <span style="color:#3271a5">Key Features</span>
- **Standard Graphical User Interface (GUI)**

  <span style="color:white">The GUI offers a simple yet efficient interface, allowing users to upload PDFs for processing. It also enables users to specify a destination path where the generated JSON file will be saved.


- **Automated Document Processing**  
  <span style="color:white">This feature extracts and processes text from both PDF documents and images, performing tasks such as text cleaning, summarization, and image extraction. The images are decoded into base64 format, and all extracted data is organized and converted into a standardized JSON format. The resulting JSON file is then saved to the user-specified path.


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

### <span style="color:#3271a5">3. X Server </span>
If you use Windows you'll need to install X server. 
[How to Install and Run X Server in Windows 11?](https://dev.to/winsides/how-to-install-and-run-x-server-in-windows-11-4na9)

### <span style="color:#3271a5">4. Docker </span>
- Run the Application
  ```bash
  docker build -t myapp . 
  docker run -it -e DISPLAY=host.docker.internal:0.0 -p 8000:8000 myapp
  ```
- Access the app at: http://localhost:8000
- stop the Container:
  ```bash
  docker stop myapp_container
  ```
