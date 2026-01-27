# Commands for dev startup
Opening postgres without password: 

```bash
sudo -u postgres psql
```

Activating and deactivating the python virtual environment:
```bash
source venv/bin/activate
(venv) $ deactivate
```

Starting the backend from repo root:
```bash
cd backend
source venv/bin/activate
cd ..
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8001
# In production, we don't use --reload as a tag, because of limited RAM in render
```

Starting the frontend dev server
```bash
cd frontend 
npm run dev
```

Testing sql role based authentication privileges for sclub_user (in psql terminal):
```SQL
SELECT * FROM information_schema.role_table_grants WHERE grantee = 'sclub_user';
```

Generating a random string:
```python
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Axios is used to expose the backend endpoints to the frontend in [api.ts](frontend/src/services/api.ts) because the backend and frontend run in completely different locations. It acts as a bridge, letting the frontend send HTTP requests and receive JSON responses from the backend. The backend, built with FastAPI, defines the API endpoints, handles these requests, validates and parses data using Pydantic models, checks authentication via JWT tokens, interacts with the database through SQLAlchemy, and returns the appropriate responses. This separation allows the frontend to remain decoupled from the backend’s implementation while still being able to access and manipulate data securely and efficiently.

# Render
To spin up a temporary instance of the render backend service when a pull request is made, use [render preview] in the title.
