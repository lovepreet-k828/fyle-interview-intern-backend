here's the documentation on building and running the application with Docker: first go to root directory of this flask application then follow below steps

### 1. Create a Dockerfile:

Create a file named `Dockerfile` in the root directory of your Flask application with the following content:

```Dockerfile
# Use Python 3.8 slim image as base
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Set environment variables
ENV FLASK_APP=core/server.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose port 5000 to the outside world
EXPOSE 5000

# Reset the database only if the RESET_DB environment variable is set
# this example command will reset the database: docker build --build-arg RESET_DB=true -t my-flask-app-reset .

ARG RESET_DB
RUN if [ "$RESET_DB" = "true" ]; then \
        export FLASK_APP=core/server.py && \
        rm core/store.sqlite3 && \
        flask db upgrade -d core/migrations/; \
    fi

# Run the Flask application using run.sh script
CMD ["bash", "run.sh"]

```

### 2. Create a docker-compose.yml file:

Create a file named `docker-compose.yml` in the root directory of your Flask application with the following content:

```yaml
version: '3.8'

services:
  flask-app:
    build:
      context: .
    ports:
      - "7755:7755"
```

### 3. Building and Running the Application with Docker:

#### Building the Docker Image:

In [README.md file](./README.md) some commands were provided to reset the database, we can execute those commands while building docker image if want as mentioned below: 


a. **Building with Database Reset**:

```bash
docker build --build-arg RESET_DB=true -t my-flask-app .
```

This command builds the Docker image while setting the `RESET_DB` build argument to `true`, which triggers the database reset during the image build process.

b. **Building Without Database Reset**:

```bash
docker build -t my-flask-app .
```

This command builds the Docker image without setting the `RESET_DB` build argument, so the database reset commands specified in the Dockerfile won't be executed during the image build process.


### 4. Running the Docker Container:

Once the Docker image is built, you can run the Docker container by using below command:

```bash
docker compose up
```

This command starts the Docker container based on the configuration specified in the `docker-compose.yml` file. Your Flask application will be accessible at `http://localhost:7755`.
