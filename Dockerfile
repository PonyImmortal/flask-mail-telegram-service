# Промежуточный образ для установки зависимостей
FROM python:3.9-slim as builder

WORKDIR /install

COPY requirements.txt /requirements.txt

RUN pip install --prefix=/install --no-warn-script-location --no-cache-dir -r /requirements.txt


# Финальный образ
FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /install /usr/local

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "send_email_app:app"]

