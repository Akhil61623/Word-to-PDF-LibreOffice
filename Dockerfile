FROM python:3.11-slim

# LibreOffice install
RUN apt-get update && apt-get install -y libreoffice && apt-get clean

# Python requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app
COPY . .

CMD ["gunicorn", "app:app"]
