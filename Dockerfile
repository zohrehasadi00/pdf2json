FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    python3-tk \
    tk-dev \
    libtk8.6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["python", "main.py"]

# created images using (only once): docker build -t myapp .
# run the docker container (every time we need to): docker run -p 8000:8000 myapp