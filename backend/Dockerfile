FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system build deps and libpq for psycopg2
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    gcc \
    libpq-dev \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Install Rust toolchain into a writable location (needed for maturin/cargo builds)
ENV CARGO_HOME=/root/.cargo RUSTUP_HOME=/root/.rustup
ENV PATH=/root/.cargo/bin:$PATH
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

# Create app dir and install Python deps
WORKDIR /app
COPY backend/requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy repository (keep source outside until deps are installed)
COPY . /app

EXPOSE 8000

# Default production command (use $PORT mapping from host if needed)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "$PORT", "--workers", "1"]