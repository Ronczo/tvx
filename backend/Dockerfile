FROM  python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /backend
RUN apt-get update
RUN pip install --upgrade pip
RUN pip install poetry
COPY poetry.lock /backend/
COPY pyproject.toml /backend/
RUN poetry install
COPY . .
EXPOSE 8000
