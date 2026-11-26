FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN useradd --create-home --uid 10001 appuser
COPY --chown=appuser:appuser . .

RUN python -m pip install --upgrade pip && \
    python -m pip install .

USER appuser

# MCP uses stdio. Run with an interactive stdin, e.g. docker run -i --rm IMAGE.
CMD ["ajo-time-machine-mcp"]
