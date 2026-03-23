FROM python:3.14-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev


FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV PATH="/app/.venv/bin:$PATH"

RUN useradd -m -u 1000 pythonium
USER pythonium

COPY --from=builder --chown=pythonium:pythonium /app/.venv /app/.venv

COPY --chown=pythonium:pythonium . .

EXPOSE 25565

CMD ["python", "-m", "pythonium"]