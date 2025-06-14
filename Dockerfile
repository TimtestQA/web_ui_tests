FROM python:3.11-alpine3.20

# Установка необходимых пакетов
RUN apk update && \
    apk add --no-cache \
    chromium \
    chromium-chromedriver \
    firefox \
    firefox-esr \
    wget \
    curl \
    tar \
    openjdk11-jre

# Установка Allure
RUN curl -o allure-2.13.8.tgz -Ls https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.13.8/allure-commandline-2.13.8.tgz && \
    tar -zxvf allure-2.13.8.tgz -C /opt/ && \
    ln -s /opt/allure-2.13.8/bin/allure /usr/bin/allure && \
    rm allure-2.13.8.tgz

WORKDIR /usr/workspace
COPY ./requirements.txt /usr/workspace
RUN pip3 install -r requirements.txt