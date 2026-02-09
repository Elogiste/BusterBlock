FROM python:3.13

WORKDIR /app
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    default-libmysqlclient-dev \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

COPY dependances.txt .
RUN pip install --no-cache-dir -r dependances.txt


COPY . .

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
