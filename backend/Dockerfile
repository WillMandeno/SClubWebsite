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

# Set the working directory
WORKDIR /app

# Copy the backend directory into the container
COPY . /app/backend/

# Install dependencies
COPY requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Set the Python path to include the /app directory
ENV PYTHONPATH=/app

# Expose the port your app runs on
EXPOSE 8000

# Default production command
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"]