FROM python:3.7.4

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
COPY ./setup.py ./app

WORKDIR /app

COPY zhengli ./zhengli
RUN pip install -r requirements.txt

RUN pip install -e .

COPY . /app

EXPOSE 5000

CMD ["python", "server.py"]
