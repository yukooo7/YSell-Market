import os
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = "static/images"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

async def save_image(image: UploadFile) -> str:
    ext = os.path.splitext(image.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Неподдерживаемый формат изображения")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, image.filename)

    # Сохраняем файл
    with open(file_path, "wb") as buffer:
        content = await image.read()
        buffer.write(content)

    # Формируем URL для фронта с прямыми слэшами
    file_url = f"/static/images/{image.filename}".replace("\\", "/")

    return file_url
