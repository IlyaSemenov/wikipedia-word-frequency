FROM python:3.9-slim

# Install system dependencies required by wikiextractor and the download script
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application scripts
COPY gather_wordfreq.py .
COPY wiki-dump.sh .
RUN chmod +x wiki-dump.sh

# Create a data directory and set it as the default working directory
WORKDIR /data