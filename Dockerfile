FROM python:3.10-slim

# Biar Python gak bikin sampah .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# 1. Bikin user dulu (Rakyat Biasa)
RUN useradd -m putri

# 2. Copy & Install bumbu (requirements)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. COPY file secara spesifik (Gak boleh pakai titik-titik)
# Kita copy sebagai root dulu sebentar biar bisa dikunci
COPY manage.py .
COPY core/ ./core/
COPY config/ ./config/

# 4. JURUS PAMUNGKAS: Kunci semua pintu!
# - Ubah pemilik semua file jadi 'putri'
# - 'find' akan mencari semua folder (-d) dan kasih izin 555 (Read-Execute)
# - 'find' akan mencari semua file (-f) dan kasih izin 444 (Read-Only)
RUN chown -R putri:putri /app && \
    find /app -type d -exec chmod 555 {} + && \
    find /app -type f -exec chmod 444 {} +

# 5. Kalau Django butuh nulis sesuatu (misal database lokal), buka satu lubang kecil saja
# Jika kamu pakai PostgreSQL, bagian ini bisa dihapus.
RUN touch /app/db.sqlite3 && chmod 664 /app/db.sqlite3 && chown putri:putri /app/db.sqlite3

USER putri

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]