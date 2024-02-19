# Use an official Python runtime as a parent image
FROM python:3.11.7

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

RUN pip install -e .

# # Install Poetry
# RUN pip install poetry

# # Use Poetry to install dependencies
# RUN poetry config virtualenvs.create false \
#   && poetry install --no-interaction --no-ansi

ENTRYPOINT [ "streamsync", "run" ]
# Make port 5000 available to the world outside this container
EXPOSE 5000
# Run the command to start your application
CMD [ "src/stocksai/ui/",  "--port", "5000", "--host", "0.0.0.0" ]