# ETAP 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt

COPY app/ ./app/

# ETAP 2: Test
FROM builder as test

ENV PATH=/root/.local/bin:$PATH

RUN pytest app/tests/

# ETAP 3: Final
FROM python:3.11-slim as final

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

COPY --from=builder /app/app ./app

EXPOSE 5000

# Command to run the application using Gunicorn (a production-ready web server)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app.src.app:app"]
