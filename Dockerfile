FROM python:3.9-slim

#
RUN apt-get update && \
    apt-get install -y openssl && \
    rm -rf /var/lib/apt/lists/*

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install  -r /code/requirements.txt

#
COPY . /code/app
WORKDIR /code/app

#
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]