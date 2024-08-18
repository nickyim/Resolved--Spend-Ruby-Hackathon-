# Base image
FROM python:3.12-slim-bullseye

# Set working directory
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    swig \
    gcc \
    build-essential \
    libpulse-dev

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy the rest of the application files
COPY . .

# Command to run the application (replace with your actual command)
CMD ["python", "app.py"]
