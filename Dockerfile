# Use Python 3.9 as base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /data

# Expose port
EXPOSE 8000

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0

# Clone repo into folder
RUN git clone https://github.com/vankizmann/coloa.git .

# Install yolov5 weights
RUN git clone https://github.com/ultralytics/yolov5.git ./yolov5

# Update pip
RUN python -m pip install --upgrade pip

# Install pip dependencies
RUN pip install --upgrade --no-cache-dir -r requirements.txt

# Run unvicorn
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]