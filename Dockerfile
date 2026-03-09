FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt


FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    APP_HOST=0.0.0.0 \
    APP_PORT=8000

WORKDIR /app

RUN groupadd --system app && \
    useradd --system --gid app --create-home --home-dir /home/app app

COPY --from=builder /opt/venv /opt/venv
COPY app ./app

RUN mkdir -p uploads && chown -R app:app /app /home/app

EXPOSE 8000

USER app

CMD ["sh", "-c", "uvicorn app.main:app --host ${APP_HOST} --port ${APP_PORT}"]
