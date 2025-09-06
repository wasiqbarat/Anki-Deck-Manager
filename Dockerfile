FROM python:3.12-slim

# Environment for faster, cleaner containers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Streamlit default port
EXPOSE 8501

# Bind to 0.0.0.0 for Docker networking
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=8501"]