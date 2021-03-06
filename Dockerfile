FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /app/api
# Install pipenv and compilation dependencies
# RUN pip install pipenv
# RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install python dependencies in /.venv
# COPY Pipfile .
# COPY Pipfile.lock .
# RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy
ADD requirements.txt .
RUN python -m pip install -r requirements.txt


COPY . ./
EXPOSE 8000