FROM python:3.10-slim

# Optimasi Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# 1. Bikin user putri
RUN useradd -m putri

# 2. Install Requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy Code secara Eksplisit (Biar gak kena recursive issue)
COPY manage.py .
COPY core/ ./core/
COPY config/ ./config/

# 4. KUNCI MATI (READ-ONLY) UNTUK CODE
# Semua file codingan kita kunci jadi 444 (Read Only buat semua)
# Folder kita kasih 555 (Read + Execute buat masuk folder)
RUN chown -R putri:putri /app && \
    find /app -type d -exec chmod 555 {} + && \
    find /app -type f -exec chmod 444 {} +

# 5. KUNCI KHUSUS DATABASE (SOLUSI DARI ERROR TERAKHIR)
# Kita pakai 600 (rw-------). 
# Artinya: Cuma 'putri' yang boleh Baca+Tulis. Group & Others = 0 (DILARANG MASUK).
RUN touch /app/db.sqlite3 && \
    chown putri:putri /app/db.sqlite3 && \
    chmod 600 /app/db.sqlite3

USER putri

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]