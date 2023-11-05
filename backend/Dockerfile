# Use the official Python 3.10 image from Docker Hub, based on Debian Buster
FROM python:3.10.2-buster

# Set the working directory inside the container
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the Python requirements file into the container
COPY ./requirements.txt /usr/src/app/requirements.txt

# Install system dependencies required for Python packages like pandas
RUN set -eux \
    && apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
       libssl-dev libffi-dev \
       libpq-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /usr/src/app/requirements.txt \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/* /root/.cache/pip

# Copy the rest of the application's code into the container
COPY . /usr/src/app/

# Expose the port the app runs on
EXPOSE 5500

# Add execution permissions to the entrypoint script
RUN chmod +x /usr/src/app/entrypoint.sh

# Set the default command to execute when creating a new container
CMD ["sh", "/usr/src/app/entrypoint.sh"]


