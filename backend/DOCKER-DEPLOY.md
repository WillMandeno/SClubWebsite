# Docker build & deploy (backend)

This document shows how to build and run the backend Docker image locally and how to deploy it to a container host (e.g. Render using a Docker deployment).

## Build locally

From the repo root:

```bash
docker build -f backend/Dockerfile -t sclub-backend:latest .
```

Then run (map port 8000):

```bash
docker run --rm -p 8000:8000 \
  -e DATABASE_URL='postgresql://sclub_user:J26Club@localhost:5432/sclub_calendar' \
  -e SECRET_KEY='qz_rp9vLhv33xp--lu1Yt3AZgZpTRCJE-yCJNRzqUYU' \
  sclub-backend:latest
```

Open http://localhost:8000/health to verify the service.

## Create admin / initialize DB

Run the initialization script against the database (from host or via container):

```bash
# Run inside a container (one-off) using the built image
docker run --rm \
  -e DATABASE_URL='postgresql://sclub_user:J26Club@localhost:5432/sclub_calendar' \
  -e ADMIN_PASSWORD='password' \
  sclub-backend:latest \
  python -m backend.scripts.create_admin
```

Or run the same command locally using your Python venv once `DATABASE_URL` is set.

## Deploy to Render (Docker)

1. In Render dashboard, create a new **Web Service** and pick **Docker**.
2. Connect your GitHub repo and select the branch to deploy.
3. Set the Dockerfile path to `backend/Dockerfile` (Render will use your repo root as context).
4. Add environment variables in the Render service settings:
   - `DATABASE_URL` (your managed Postgres connection string)
   - `SECRET_KEY` (JWT secret)
   - `ACCESS_TOKEN_EXPIRE_MINUTES` (optional)
   - `ADMIN_PASSWORD` (optional, for create-admin script)
5. Deploy. After the service is up, run the one-off command on Render to initialize the DB:
   `python -m backend.scripts.create_admin`

## Notes
- The Dockerfile installs the Rust toolchain so packages that require `maturin`/`cargo` can build during `pip install`.
- For production, you may want to pin the Rust toolchain or create a multi-stage Dockerfile to reduce image size.
- If you prefer not to use Docker on Render, you can use the host build command solution, but Docker gives reproducible builds and avoids read-only filesystem issues.
