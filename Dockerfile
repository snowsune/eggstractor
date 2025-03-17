FROM python:3.10

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:5000"]