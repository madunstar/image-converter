from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
from pillow_heif import register_heif_opener
import io
import os

# Daftarkan pembaca HEIC ke dalam Pillow
register_heif_opener()

app = FastAPI(title="Kantor Image Converter")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse(request=request,name="index.html")

@app.post("/convert/")
async def convert_image(file: UploadFile = File(...)):
    try:
        # 1. Baca file yang diupload ke dalam memory
        contents = await file.read()
        image_stream = io.BytesIO(contents)
        
        # 2. Buka gambar menggunakan Pillow (Otomatis mendeteksi HEIC/WEBP)
        img = Image.open(image_stream)
        
        # 3. Konversi ke mode RGB (Syarat wajib untuk JPG, menghilangkan transparansi/alpha channel)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        elif img.mode != "RGB":
            img = img.convert("RGB")
            
        # 4. Siapkan penampung untuk gambar hasil konversi
        output_stream = io.BytesIO()
        
        # 5. Simpan gambar ke penampung dalam format JPEG dengan kualitas tinggi
        img.save(output_stream, format="JPEG", quality=95)
        output_stream.seek(0)
        
        # 6. Siapkan nama file baru
        original_filename = file.filename
        new_filename = original_filename.rsplit(".", 1)[0] + ".jpg"
        
        # 7. Kirim kembali ke client sebagai file download
        headers = {
            'Content-Disposition': f'attachment; filename="{new_filename}"'
        }
        
        return StreamingResponse(output_stream, media_type="image/jpeg", headers=headers)
        
    except Exception as e:
        return {"error": f"Gagal mengonversi gambar: {str(e)}"}