import os
import uuid
from fastapi import UploadFile, HTTPException

# Разрешенные форматы
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

# Базовая директория для аватарок
UPLOAD_DIR = "static/images/avatars"

async def save_avatar(image: UploadFile) -> str:
    # Получаем расширение файла
    ext = os.path.splitext(image.filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Неподдерживаемый формат изображения")

    # Создаем директорию, если нет
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Генерируем уникальное имя файла
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Сохраняем файл
    with open(file_path, "wb") as buffer:
        content = await image.read()
        buffer.write(content)

    # Генерируем URL для клиента
    file_url = f"/static/images/avatars/{unique_filename}".replace("\\", "/")

    return file_url
