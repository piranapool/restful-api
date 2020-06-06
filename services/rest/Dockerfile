# retrieve base image
FROM python:3.8.1-slim-buster

# define work directory
WORKDIR /usr/src/app

# define environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update && apt-get install -y netcat
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# install app
COPY . /usr/src/app/

# run entrypoint
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
