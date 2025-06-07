# Backend Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY *.py .
COPY .email_config.enc* ./
COPY .config_salt* ./

# Expose port
EXPOSE 5001

# Run the application
CMD ["python", "email_api.py"] 