# Use Python 3.11 as base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /data

# Copy the current directory contents into the container at /app
COPY . /data

# Command to run the Python script
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["fastapi", "/data/main.py", "--port", "80"]