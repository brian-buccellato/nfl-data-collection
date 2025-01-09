FROM python:3.12

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/"

WORKDIR /usr/src/app

COPY . .

RUN pip install --upgrade pip && pip install pipenv
RUN pipenv install --ignore-pipfile --system