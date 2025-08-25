FROM python:3.10-slim

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

# Create odoo system user
RUN useradd -m -d ${ODOO_HOME} -U -r -s /bin/bash ${ODOO_USER}

# Copy Odoo source code into container
WORKDIR ${ODOO_HOME}
ENV ODOO_VERSION=17.0

# Clone Odoo from GitHub
RUN git clone --depth 1 --branch ${ODOO_VERSION} https://github.com/odoo/odoo.git odoo

# Install Python dependencies
RUN pip install --upgrade pip wheel setuptools 
    # pip install -r /opt/odoo/odoo/requirements.txt

# Create directories for custom addons, config, logs, data
RUN mkdir /opt/odoo/extra-addons /var/log/odoo /var/lib/odoo && \
    chown -R odoo:odoo /opt/odoo /var/log/odoo /var/lib/odoo

# COPY . ${ODOO_HOME}
# Copy config
COPY ./config/odoo.conf ${ODOO_RC}

# Copy requirements
COPY requirements.txt ${ODOO_HOME}
COPY dev_requirements.txt ${ODOO_HOME}

# Copy addons
COPY ./extra_addons ${ODOO_HOME}

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r dev_requirements.txt

# Ensure correct permissions
RUN chown -R ${ODOO_USER}:${ODOO_USER} ${ODOO_HOME}

USER ${ODOO_USER}

# Expose Odoo port
EXPOSE 8069

# Default command
CMD ["python", "odoo/odoo-bin", "-c", "/etc/odoo/odoo.conf"]
