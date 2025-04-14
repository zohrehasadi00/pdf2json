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
COPY . .

EXPOSE 8000
CMD ["python", "main.py"]

# created images using (only once): docker build -t myapp .
# run the docker container (every time we need to): docker run -p 8000:8000 myapp
# docker run -it -e DISPLAY=host.docker.internal:0.0 -p 8000:8000 myapp
# echo $DISPLAY