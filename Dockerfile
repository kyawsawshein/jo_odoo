FROM python:3.13-slim

# Environment variables
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    ODOO_USER=odoo \
    ODOO_HOME=/opt/odoo \
    ODOO_RC=/etc/odoo/odoo.conf

# System dependencies for Odoo & Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Tools
    bash git curl wget \
    # Build tools
    build-essential \
    # Libraries required by Odoo addons
    libpq-dev \
    libxml2-dev libxslt1-dev \
    libjpeg-dev zlib1g-dev \
    libldap2-dev libsasl2-dev \
    libffi-dev \
    # JS runtime (needed for assets pipeline)
    nodejs npm \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    fontconfig \
    libxrender1 \
    xfonts-base \
    xfonts-75dpi \
    libjpeg62-turbo \
    libxext6 \
    libx11-6 && \
    rm -rf /var/lib/apt/lists/*

# Install a patched version of wkhtmltopdf (version 0.12.6.1) that is compatible with Odoo 19 (which is based on Debian Bookworm).
# NOTE: The official Debian version (0.12.6) may not support headers/footers.
# This downloads a build compatible with Bookworm/Debian 12.
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.bookworm_amd64.deb && \
    apt-get install -y --allow-downgrades ./wkhtmltox_0.12.6.1-3.bookworm_amd64.deb && \
    rm wkhtmltox_0.12.6.1-3.bookworm_amd64.deb

# Create odoo system user
RUN useradd -m -d ${ODOO_HOME} -U -r -s /bin/bash ${ODOO_USER}

# Copy Odoo source code into container
WORKDIR ${ODOO_HOME}
ENV ODOO_VERSION=19.0

# Clone Odoo from GitHub
RUN git clone --depth 1 --branch ${ODOO_VERSION} https://github.com/odoo/odoo.git odoo

# Install Python dependencies
RUN pip install --upgrade pip wheel setuptools 
# pip install -r /opt/odoo/odoo/requirements.txt

# Create directories for custom addons, config, logs, data
RUN mkdir /opt/odoo/odoo_extra_addons /opt/odoo/extra_addons /opt/odoo/vendor_addons /var/log/odoo /var/lib/odoo && \
    chown -R odoo:odoo /opt/odoo /var/log/odoo /var/lib/odoo

# COPY . ${ODOO_HOME}
# Copy config
COPY ./config/odoo.conf ${ODOO_RC}

# Copy requirements
COPY requirements.txt ${ODOO_HOME}
# COPY dev_requirements.txt ${ODOO_HOME}

# Copy vandor addons
# COPY vendor_addons ${ODOO_HOME}/vendor_addons

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install --no-cache-dir -r dev_requirements.txt

# Ensure correct permissions
RUN chown -R ${ODOO_USER}:${ODOO_USER} ${ODOO_HOME}

USER ${ODOO_USER}

# Expose Odoo port
EXPOSE 8090

# Default command
CMD ["python", "odoo/odoo-bin", "-c", "/etc/odoo/odoo.conf"]
