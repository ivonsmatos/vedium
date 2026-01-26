FROM python:3.14-slim-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    mariadb-client \
    redis-tools \
    build-essential \
    libmariadb-dev \
    libssl-dev \
    libcrypto++-dev \
    python3-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    tcl8.6-dev \
    tk8.6-dev \
    python3-tk \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1-dev \
    xvfb \
    libfontconfig1 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 24 and Yarn
# Using nodesource script for Node.js 24
RUN curl -fsSL https://deb.nodesource.com/setup_24.x | bash - \
    || curl -fsSL https://deb.nodesource.com/setup_current.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g yarn

# Install Bench
RUN pip install frappe-bench

# Create frappe user
RUN useradd -ms /bin/bash frappe
USER frappe
WORKDIR /home/frappe

# Expose ports for dev
EXPOSE 8000 9000 8001

CMD ["sleep", "infinity"]
