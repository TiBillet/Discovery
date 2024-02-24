FROM python:3.10-bullseye

## UPDATE
RUN apt-get update && apt-get upgrade -y
# Install app
RUN apt-get install -y nano iputils-ping curl borgbackup cron

RUN useradd -ms /bin/bash poetry_user
USER poetry_user

ENV POETRY_NO_INTERACTION=1

## PYTHON
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/home/poetry_user/.local/bin:$PATH"

COPY --chown=poetry_user:poetry_user ./ /DjangoFiles
WORKDIR /DjangoFiles
RUN poetry install

# ENTRYPOINT ["poetry", "run"]
# docker build -t tibillet/primarylink:latest .
# docker push tibillet/primarylink:latest