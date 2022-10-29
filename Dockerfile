FROM python:3.11.0-slim

WORKDIR /app

RUN apt update \
    && apt install -y git

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /app/

USER 1000

CMD ["python3", "main.py"]
