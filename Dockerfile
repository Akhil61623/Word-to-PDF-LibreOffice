FROM python:3.10-slim

# Install LibreOffice
RUN apt-get update && apt-get install -y libreoffice && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy app
COPY . .

# Run app with gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
