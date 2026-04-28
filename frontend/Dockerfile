# 1. Base Image
FROM python:3.10-slim

# 2. Global Settings
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# 3. Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 4. Copy Dependencies
COPY pyproject.toml .

# 5. Install (System-wide)
# --system: Installs to /usr/local/lib/python3.10/site-packages
# --no-cache: Keeps the image small
RUN uv pip install --system --no-cache -r pyproject.toml

# 6. Copy App Code
COPY . .

# 7. Launch
EXPOSE 5001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]
