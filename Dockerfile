FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    python3-tk \
    tk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download all punkt-related data to a known location
RUN python -m nltk.downloader -d /usr/local/nltk_data punkt
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"

# Ensure environment variable is set for runtime
ENV NLTK_DATA=/usr/local/nltk_data

COPY . .

EXPOSE 8000
CMD ["python", "main.py"]


# Power shell:
#  cd C:\Users\zohre\bachelorT\pdf2json
#
# docker build -t myapp .
#
# docker run -it `
#   -e DISPLAY=host.docker.internal:0.0 `
#   -p 8000:8000 `
#   -v ${PWD}\results:/app/results `
#   myapp
#
#
#
#  Get-ChildItem .\results
# Get-Content "C:\Users\zohre\bachelorT\pdf2json\results\narkose.json"
