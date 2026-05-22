# serzh-ii-kadr
# Серж-ИИ-Кадр

Веб-бот для подготовки кадровых документов.

## Локальный запуск
```bash
pip install -r requirements.txt
python app.py
```

Откройте: http://127.0.0.1:5000

## Деплой на Render
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
