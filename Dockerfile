FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app/__init__.py
ENV FLASK_ENV=development
ENV DEMO_MODE=true

EXPOSE 12000

CMD ["gunicorn", "--bind", "0.0.0.0:12000", "--access-logfile", "-", "--error-logfile", "-", "app:create_app()"]