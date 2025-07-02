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

# Bypass proxy for ollama.com
ENV NO_PROXY=ollama.com
ENV no_proxy=ollama.com

# Install Ollama (with retries and HTTP/1.1, and unset proxy)
RUN unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY && \
    curl --retry 5 --http1.1 -fsSL -o install.sh https://ollama.com/install.sh && \
    bash install.sh && \
    rm install.sh

# Create app directory
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "ollama serve & sleep 5 && streamlit run streamlit_app.py"]
