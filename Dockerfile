# Use a small official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system deps (if needed) and pip dependencies
# (Add apt-get lines only if you need system packages)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy project files (model, app, templates, static)
COPY . .

# Expose port uvicorn will use
EXPOSE 8000

# Start the app with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
