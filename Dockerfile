# 1) Base image
FROM python:3.11-slim

# 2) Runtime/env hygiene
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3) Workdir
WORKDIR /app

# 4) Install deps first (better layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5) Copy app code
COPY . .

# 6) Flask entry (change to your main file if different)
ENV FLASK_APP=app.py

# 7) Expose the Flask port
EXPOSE 5000

# 8) Run the app (use flask CLI so host/port are explicit)
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
