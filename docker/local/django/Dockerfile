FROM python:3.10.0-slim-buster

#  Defines an environment variable APP_HOME with the value "/app". This variable is used as the main directory for the application.
ENV APP_HOME=/app
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME

# Defines an environment variable APP_HOME with the value "/app". This variable is used as the main directory for the application.
LABEL maintainer='bilvad1@gmail.com'
LABEL decription="Development image for Real Estate Project"

# Prevents Python from writing pyc files to disk (bytecode).
ENV PYTHONDONTWRITEBYTECODE 1

# Ensures that Python output is sent straight to terminal without buffering it first.
ENV PYTHONUNBUFFERED 1

# Installs system dependencies and cleans up the package manager cache to reduce the image size.
RUN apt-get update \
  && apt-get install -y build-essential \
  && apt-get install -y libpq-dev \
  && apt-get install -y gettext \
  && apt-get -y install netcat gcc postgresql \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

# Copies the requirements.txt file from the host to the /app directory in the image.
COPY ./requirements.txt /app/requirements.txt 

RUN pip3 install -r requirements.txt

#  Copies the entrypoint script from the host to the /entrypoint directory in the image.
COPY ./docker/local/django/entrypoint /entrypoint
# Convert Windows lines to Unix lines for shell scripts
RUN sed -i 's/\r$//g' /entrypoint
# Make the entrypoint script executable
RUN chmod +x /entrypoint

COPY ./docker/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# In the provided Dockerfile, the ENTRYPOINT [ "/entrypoint"] line specifies that the script located at /entrypoint will be the default command executed when the container is started. 
ENTRYPOINT [ "/entrypoint"]
