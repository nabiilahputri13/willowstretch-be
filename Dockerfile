FROM python:3.10-slim

# 1. Tambahkan environment variable agar Python tidak lambat (buffer)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# 2. Bikin "Rakyat Biasa" (User baru) agar tidak pakai Root
# Kita beri nama user-nya 'putri'
RUN useradd -m putri && chown -R putri /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy semua file tapi kasih izin akses ke user 'putri'
COPY --chown=putri:putri . .

# 4. Pindah dari Raja (root) ke Rakyat Biasa (putri)
USER putri

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]