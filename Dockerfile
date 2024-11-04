FROM python:3.12.0-slim

ARG install_dev_packages

WORKDIR /app

COPY ./Pipfile* /app/

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install pipenv && \
    python3 -m pipenv install --system

COPY ./api /app/api
COPY ./init.sh /app/

CMD ["/bin/bash","init.sh"]