# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install wkhtmltopdf dependencies
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    libxrender1 \
    libfontconfig1 \
    libx11-dev \
    && apt-get clean

# Create a directory for the app
WORKDIR /app

# Copy the application files
COPY . /app

# Install the Python dependencies
RUN pip install poetry
RUN poetry install

# Expose port for easier debugging (optional)
EXPOSE 5000

# Change the entrypoint script permissions
RUN chmod +x entrypoint.sh

# Run the Python application
CMD ["./entrypoint.sh", "python", "src/app.py"]