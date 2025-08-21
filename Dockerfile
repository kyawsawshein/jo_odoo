FROM ubuntu:22.04

# Install system dependencies
RUN apt-get update && apt-get install -y libssl-dev python3-dev \
    git wget curl python3.10 python3.10-venv python3.10-dev \
    build-essential libpq-dev libxml2-dev libxslt1-dev libjpeg-dev \
    libldap2-dev libsasl2-dev libffi-dev node-less xz-utils \
    && rm -rf /var/lib/apt/lists/*

# Create Odoo user
RUN useradd -m -d /opt/odoo -U -r -s /bin/bash odoo
WORKDIR /opt/odoo
USER odoo

# Create virtual environment
RUN python3.10 -m venv odoo-venv
ENV VIRTUAL_ENV=/opt/odoo/odoo-venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Upgrade pip and build tools
RUN pip install --upgrade pip setuptools wheel cython
RUN pip install cryptography pyopenssl cffi gevent==22.10.2 greenlet==2.0.2

# Clone Odoo 17 CE
RUN git clone --depth 1 --branch 17.0 https://github.com/odoo/odoo.git odoo

# get requirement.txt
COPY requirements.txt /opt/odoo/
COPY dev_requirements.txt /opt/odoo/

# Install all other Odoo requirements
RUN grep -v -E "gevent|greenlet" odoo/requirements.txt > odoo/requirements_filtered.txt
RUN pip install --no-cache-dir -r /opt/odoo/requirements.txt --no-deps
RUN pip install --no-cache-dir -r /opt/odoo/dev_requirements.txt --no-deps

# Install missing common packages
RUN pip install six pytz babel lxml psycopg2-binary passlib certifi requests urllib3 idna charset-normalizer geoip2 zeep attrs requests-file cached-property openpyxl

# Copy custom addons
COPY ./extra_addons /opt/odoo/extra-addons

# Copy config
COPY ./config/odoo.conf /opt/odoo/odoo.conf

# Create session directory and give ownership to odoo user
RUN mkdir -p /opt/odoo/data && chown -R odoo:odoo /opt/odoo/data

# Expose Odoo port
EXPOSE 8069

# Start Odoo
# CMD ["odoo/odoo-bin", "-c", "odoo.conf"]
