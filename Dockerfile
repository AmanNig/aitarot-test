FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    lsb-release \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    python3-pip \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Symlink python3.11
RUN ln -sf /usr/bin/python3.11 /usr/bin/python

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | bash

# Create app directory
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_A.txt

CMD ["sh", "-c", "ollama serve & sleep 5 && streamlit run streamlit_app.py"]
