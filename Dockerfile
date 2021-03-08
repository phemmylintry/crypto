FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

# RUN apt-get update && apt-get upgrade -y \
#     && apt-get install -y --no-install-recommends \
#     && apt-get install -y mariadb-client \
#     && rm -rf /var/lib/apt/lists/*

WORKDIR /app/api
# # Install pipenv and compilation dependencies
# RUN pip install pipenv
# RUN apt-get update && apt-get install -y --no-install-recommends gcc

# # Install python dependencies in /.venv
# COPY Pipfile .
# COPY Pipfile.lock .
# RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . ./
CMD gunicorn crypto_transaction.wsgi --log-file -