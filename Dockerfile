FROM python:3.11.10

#создание переход в рабочую дерикторию в образе
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
#указание пути и копирование файлов откуда"." и куда"."
COPY . .

#команда для запуска контейнера
#CMD ["python",  "src/main.py"]
CMD alembic upgrade head; python src/main.py