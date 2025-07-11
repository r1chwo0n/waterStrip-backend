from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import cloudinary
import cloudinary.uploader
import uuid
import os
from dotenv import load_dotenv

load_dotenv()  # โหลดตัวแปรจาก .env

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

app = FastAPI()

@app.post("/api/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # อ่านเนื้อไฟล์จาก UploadFile
        contents = await file.read()

        # สร้างชื่อแบบสุ่ม
        unique_name = f"strip_{uuid.uuid4().hex}"

        # อัปโหลดไป Cloudinary
        result = cloudinary.uploader.upload(contents, public_id=unique_name)

        # ส่ง URL กลับไปให้ frontend
        return {
            "msg": "Upload successful",
            "url": result["secure_url"]  # <-- frontend เอา URL นี้ไปใช้ต่อ
        }
    except Exception as e:
        return JSONResponse(content={"msg": "Upload failed", "error": str(e)}, status_code=500)
