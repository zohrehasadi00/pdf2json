#for being lightweight
# TODO: should i use "Shared" or "Simple" tags?
# following is from Simple Tags -> https://hub.docker.com/_/python/?tab=description&name=3.10-slim
FROM python:3.13-slim-bullseye

USER root

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \  # For working with PDFs (e.g., extracting text)
    && rm -rf /var/lib/apt/lists/*  # Clean up apt cache to reduce image size

# Install requirements file
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# TODO: Is this correct?
# access the pipeline
COPY . /app

# this should set the working directory
WORKDIR /app

# Optional (from internet)
# create a non-root user for better security
ARG USERID=1000
ARG GROUPID=1000
RUN groupadd -g $GROUPID appuser && useradd -m -u $USERID -g $GROUPID appuser
USER appuser

# run the application
ENTRYPOINT ["python", "main.py"]
# docker compose
