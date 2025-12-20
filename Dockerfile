FROM python:3.14-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock /app/

WORKDIR /app

COPY . /app
RUN uv sync --locked

ENV UV_NO_DEV=1
ENV PATH="/app/.venv/bin:$PATH"

CMD ["ogurec"]