FROM python:3.9-slim
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /var/www/app/
COPY . .
CMD ["python", "app.py"]
