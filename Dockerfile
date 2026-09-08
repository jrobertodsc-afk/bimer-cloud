FROM python:3.11-slim

WORKDIR /app

# Instala dependencias a partir do backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia codigo completo
COPY backend/ ./backend/
COPY database/ ./database/

ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port ${PORT:-8000}"]
