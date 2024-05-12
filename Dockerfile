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
