import shutil

from fastapi import APIRouter, UploadFile

from src.services.images import ImageService
from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("")
def upload_image(file: UploadFile):
    ImageService().upload_image(file)


"""
ПРимер бэк таски на фастапи. Подходит для задач без обработки 
больших объемов инфы ( отправить письмо и тд
@router.post("")
def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    image_path = f"src/static/images/{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    background_tasks.add_task(resize_image, image_path)
"""
