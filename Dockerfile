# Menggunakan base image Python yang ringan
FROM python:3.10-slim

# Mencegah Python membuat file .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# Memastikan output terminal tidak tertahan (berguna untuk logging)
ENV PYTHONUNBUFFERED 1

# Menentukan direktori kerja di dalam container
WORKDIR /app

# Menyalin file requirements dan menginstalnya
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh file proyek ke dalam container
COPY . .

# Menjalankan server uvicorn pada port 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]