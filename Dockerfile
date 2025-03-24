ARG PYTHON_VERSION=3.11.11
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev \
    default-libmysqlclient-dev \
    build-essential \
    python3-dev

USER root
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    firefox-esr \
    libx11-xcb1 \
    libxtst6 \
    libxrender1 \
    libdbus-glib-1-2 \
    libgtk-3-0 \
    libasound2 \
    fonts-liberation \
    libgl1-mesa-dri \
    libpci3 \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /tmp/cache/fontconfig && chmod 777 /tmp/cache/fontconfig
ENV FONTCONFIG_PATH=/tmp/cache/fontconfig

RUN case $(dpkg --print-architecture) in \
    amd64) ARCH=linux64 ;; \
    arm64) ARCH=linux-aarch64 ;; \
    *) echo "Unsupported architecture" && exit 1 ;; \
    esac && \
    wget -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-$ARCH.tar.gz && \
    tar -xvzf /tmp/geckodriver.tar.gz -C /usr/local/bin/ && \
    chmod +x /usr/local/bin/geckodriver && \
    rm /tmp/geckodriver.tar.gz

RUN apt-get update && apt-get install -y \
    cron \
    vim \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/run /var/log && \
    chmod 0755 /var/run /var/log && \
    touch /var/run/crond.pid && \
    chmod 0644 /var/run/crond.pid && \
    touch /var/log/cron.log && \
    chmod 0644 /var/log/cron.log

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

COPY cronjob /etc/cron.d/crypto-cron

RUN chmod 0644 /etc/cron.d/crypto-cron && crontab /etc/cron.d/crypto-cron

RUN crontab /etc/cron.d/crypto-cron

CMD ["cron", "-f"]


