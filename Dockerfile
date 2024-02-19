# Use an official Python runtime as a parent image
FROM python:3.11.0a1-slim

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install Poetry
RUN pip install -e .

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the command to start your application
CMD ["python", "streamsync", "run", "--port", "80"]