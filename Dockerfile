FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# 1. Bikin user dulu
RUN useradd -m putri

# 2. Copy requirements (Ini aman pakai root sebentar)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. AMBIL HANYA YANG PERLU (Menjawab "Copying recursively")
# Ganti 'core', 'config', dll dengan nama folder project Django kamu
COPY --chown=putri:putri --chmod=555 manage.py .
COPY --chown=putri:putri --chmod=555 core/ ./core/
COPY --chown=putri:putri --chmod=555 config/ ./config/

# 4. Buat folder untuk file statis/media yang butuh izin tulis (Jika perlu)
RUN mkdir -p /app/staticfiles && chown putri:putri /app/staticfiles

# 5. Pindah ke user putri
USER putri

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]