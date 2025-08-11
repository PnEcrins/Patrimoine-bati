#!/bin/bash

sudo apt update
sudo apt install -y \
    python3-pip python3-venv libpq-dev python3-dev binutils libproj-dev gdal-bin \
    libjpeg62 zlib1g-dev libcairo2 libpango-1.0-0 libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 libffi-dev shared-mime-info postgresql-15-postgis-3