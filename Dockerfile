# 1. Kita ambil "Piring Kosong" (Base Image) yang udah ada Python-nya
FROM python:3.10-slim

# 2. Kita tentukan "Meja Kerja" di dalam Docker
WORKDIR /app

# 3. Salin "Daftar Belanjaan" dari laptop ke dalam Docker
COPY requirements.txt .

# 4. Suruh Docker "Belanja/Install" sesuai daftar tadi
RUN pip install --no-cache-dir -r requirements.txt

# 5. Salin "Semua Kode Project" kamu ke dalam Docker
COPY . .

# 6. Perintah terakhir: "Nyalakan Kompor!" (Jalankan server Django)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]