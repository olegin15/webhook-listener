FROM python:3.11-slim-bullseye

RUN apt-get update -qq && apt-get install -qqy \
    apt-transport-https \
    ca-certificates \
    curl \
    lxc \
    iptables

RUN curl -sSL https://get.docker.com/ | sh    

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /app
COPY . /app

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]