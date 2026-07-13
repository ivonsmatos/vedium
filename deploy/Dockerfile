# Vedium production runtime overlay for Frappe/ERPNext v16.
#
# Raven needs:
# - gcc/build-essential to compile blurhash-python on Python 3.14;
# - Node 24 + Yarn to build its React/Vite assets.
#
# The base image remains the official ERPNext v16 image; this layer only adds
# build/runtime tooling required by the installed apps.

FROM frappe/erpnext:v16

USER root

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg \
        gcc \
        g++ \
        build-essential \
        pkg-config \
    && curl -fsSL https://deb.nodesource.com/setup_24.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    # A imagem base mantém um NVM_DIR do usuário frappe. Sem --prefix, o npm
    # coloca o Yarn dentro desse diretório, que não entra no PATH do runtime.
    && npm install -g yarn --prefix /usr/local \
    && rm -rf /var/lib/apt/lists/*

USER frappe
