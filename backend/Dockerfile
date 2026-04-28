# Use slim for small footprint
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

# Optional: Prevents creating .pyc files (keeps container clean)
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# 1. Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 2. Copy dependencies first (Layer Caching strategy)
COPY pyproject.toml .

# 3. Install dependencies
# --system: Installs into global site-packages (no venv needed in Docker)
# --no-cache: Reduces image size
RUN uv pip install --system --no-cache -r pyproject.toml

# 4. Copy the source code (and static/ images)
COPY . .

# Documentation for the port
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
