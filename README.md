# Проект «Жук»

## Структура проекта
- `backend/` — серверная часть приложения.
- `frontend/` — клиентская часть приложения.

## Технологический стек
- **Backend**: FastAPI (Python)
- **Frontend**: Чистый HTML, CSS, JavaScript

## Запуск (предварительно)
- **Backend**:
  1. Создайте виртуальное окружение: `python -m venv .venv`
  2. Активируйте его: `source .venv/bin/activate` (Linux/macOS) или `.venv\Scripts\activate` (Windows)
  3. Установите зависимости: `pip install -r backend/requirements.txt`
  4. Запустите сервер: `uvicorn backend.main:app --host 0.0.0.0 --port 8000`
- **Frontend**: Откройте `frontend/index.html` в браузере.

---
*Создано с помощью Gemini Code Assist*