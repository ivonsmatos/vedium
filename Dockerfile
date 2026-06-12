# Vedium Frappe — imagem de DEV (workspace bind-mount).
# Para PROD, prefira frappe_docker oficial: https://github.com/frappe/frappe_docker
# Versões alinhadas com produção (frappe/erpnext:v16 = Python 3.14 / Node 24)
# para evitar drift "funciona em dev, quebra em prod".

FROM python:3.14-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Dependências de sistema (apenas as necessárias)
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl git \
        build-essential pkg-config \
        mariadb-client \
        libmariadb-dev libssl-dev libffi-dev \
        libxml2-dev libxslt1-dev zlib1g-dev \
        libjpeg-dev libfreetype6-dev liblcms2-dev libwebp-dev \
        libharfbuzz-dev libfribidi-dev \
        wkhtmltopdf \
        redis-tools \
    && rm -rf /var/lib/apt/lists/*

# Node.js 24 (mesma major de produção) e Yarn
RUN curl -fsSL https://deb.nodesource.com/setup_24.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && npm install -g yarn \
    && rm -rf /var/lib/apt/lists/*

# Bench
RUN pip install --upgrade pip && pip install frappe-bench

# Usuário não-root
RUN useradd -ms /bin/bash frappe
USER frappe
WORKDIR /home/frappe

EXPOSE 8000 9000 8001

CMD ["sleep", "infinity"]
