FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# 1. Bikin user baru
RUN useradd -m putri

# 2. Copy requirements dulu (sebagai root, tapi nanti bisa dibaca semua)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. COPY kodingan dengan mode READ-ONLY (555)
# Ini membereskan pesan "no write permissions are assigned"
COPY --chown=putri:putri --chmod=555 . .

# 4. KECUALI untuk folder/file yang butuh nulis (seperti folder log atau DB sqlite)
# Kalau kamu pakai sqlite, user 'putri' butuh izin tulis ke folder /app dan file db
RUN chmod 755 /app && \
    touch /app/db.sqlite3 && \
    chown putri:putri /app/db.sqlite3 && \
    chmod 664 /app/db.sqlite3

USER putri

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]