import asyncio
import logging
from PIL import Image
import os
from time import sleep

from sqlalchemy.testing.plugin.plugin_base import logging

from src.database import async_session_maker_null_pool
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager


@celery_instance.task
def test_task():
    sleep(5)
    print("Я поспал")


@celery_instance.task
def resize_image(image_path: str):
    """
    Сжимает изображение до ширин 500, 300 и 200 пикселей и сохраняет их в указанную директорию.

    :param image_path: Путь к исходному изображению.
    :param output_dir: Папка для сохранения сжатых изображений.
    """
    logging.DEBUG(f"calling functions with image_path {image_path}")
    output_dir: str = "src/static/images"
    # Убедимся, что папка для сохранения существует
    os.makedirs(output_dir, exist_ok=True)

    # Загрузить изображение
    try:
        with Image.open(image_path) as img:
            original_width, original_height = img.size

            # Определяем ширины для сжатия
            target_widths = [500, 300, 200]

            for width in target_widths:
                # Рассчитать новую высоту с сохранением пропорций
                aspect_ratio = original_height / original_width
                new_height = int(width * aspect_ratio)

                # Изменить размер изображения
                resized_img = img.resize((width, new_height), Image.Resampling.LANCZOS)

                # Формируем путь для сохранения
                file_name, file_ext = os.path.splitext(os.path.basename(image_path))
                output_path = os.path.join(
                    output_dir, f"{file_name}_{width}px{file_ext}"
                )

                # Сохранить изображение
                resized_img.save(output_path)
                logging.info(f"Сохранено: {output_path}")

    except Exception as e:
        logging.error(f"Ошибка при обработке изображения: {e}")


async def get_bookings_with_today_checkin_helper():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()

        if bookings is not None:
            logging.info(f"Bookings: {bookings}")
        else:
            logging.info("No bookings found for today.")



@celery_instance.task(name="bookings_today_checkin")
def send_emails_to_users_with_today_checkin():
    asyncio.run(get_bookings_with_today_checkin_helper())
