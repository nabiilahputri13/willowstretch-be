FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# 1. User
RUN useradd -m putri

# 2. Requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy Code
COPY manage.py .
COPY core/ ./core/
COPY config/ ./config/

# 4. SECURITY CODE (Kunci Codingan)
# Kita ganti pemiliknya ke putri
RUN chown -R putri:putri /app

# JURUS SONAR DIAM:
# Kita kunci file codingan jadi 444 (Read Only) biar aman.
# TAPI folder /app kita biarkan default (755) atau set 555.
# Kenapa kita HAPUS bagian 'touch db.sqlite3'? 
# Karena nanti db.sqlite3 datangnya dari laptop kamu lewat 'docker-compose'.
RUN find /app -type f -exec chmod 444 {} + && \
    find /app -type d -exec chmod 555 {} +

USER putri

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]