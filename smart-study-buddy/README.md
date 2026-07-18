# Smart Study Buddy

# 🧠 Smart Study Buddy

An AI-powered study assistant that:
- Extracts key concepts
- Generates quiz questions
- Tracks learning progress

## 🚀 Tech Stack
- FastAPI (Backend)
- SQLite (Database)
- HTML/CSS/JS (Frontend)

## ⚙️ Setup

### 1. Clone repo
git clone <https://github.com/prashdevplayground/SilverBadgeAssignments>

### 2. Create and activate a Python virtual environment
From the `smart-study-buddy` folder:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install backend dependencies
```bash
pip install -r backend/requirements.txt
```

### 4. Start the backend server
Run from the `smart-study-buddy` root directory:
```bash
python -m uvicorn backend.app:app --reload --port 8002
```

If port `8002` is unavailable, replace it with a free port such as `8000`.

> Note: if you want to run from the `backend/` folder instead, use this command:
> ```bash
> cd backend
> python -m uvicorn app:app --reload --port 8000
> ```
> This works because `backend` is then the current package folder.

### 4.1 Run with the helper script
Make the script executable and run it from the project root:
```bash
chmod +x run.sh
./run.sh
```

If you see an error about `uvicorn` not being found, make sure the `.venv` is activated first:
```bash
source .venv/bin/activate
pip install -r backend/requirements.txt
./run.sh
```

The script will automatically activate `.venv` if present and then start the backend.

### 5. Test the backend manually
```bash
curl -v -X POST "http://127.0.0.1:8002/analyze" \
  -H "Content-Type: application/json" \
  -d '{"content":"This is a test. It covers multiple points. Learn fast."}'

curl -v -X POST "http://127.0.0.1:8002/progress" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user1","topic":"math","score":85}'

curl -v "http://127.0.0.1:8002/progress/user1"
```

### 6. Run the automated endpoint test script
```bash
python backend/test_endpoints.py
```

### 7. Open frontend
Open `frontend/index.html` in your browser.

### 8. Swagger UI
Visit:
http://127.0.0.1:8002/docs

