FROM python:3.11-slim

# Install system packages for FAISS\RUN apt-get update && \
    apt-get install -y gcc libfaiss-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir .

# Copy the entire project
COPY . .

# Expose any ports if using a web server (not needed for this CLI pipeline)
ENV PYTHONUNBUFFERED=1

# Default command: run the pipeline
CMD ["python", "-m", "minillm.pipeline"]
