FROM python:3.13.2-alpine3.21

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV PATH="/app/.venv/bin:$PATH"

COPY . /app

WORKDIR /app

RUN uv sync --frozen --no-cache --no-dev

CMD ["fastapi", "run", "app/main.py", "--port", "80", "--host", "0.0.0.0", "--root-path", "/api"]
