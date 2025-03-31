FROM python:3.9-slim

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
# ENV TF_ENABLE_ONEDNN_OPTS=0

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["python", "main.py"]

# created images using (only once): docker build -t myapp .
# run the docker container (every time we need to): docker run -p 8000:8000 myapp