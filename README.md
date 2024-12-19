# hotelsNew

# docker network creation
docker network create myNetwork

# database docker creation
docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=master \
    -e POSTGRES_PASSWORD=fs9f8a09d8fd98s0fd98gk98we! \
    -e POSTGRES_DB=booking \
    --network=myNetwork \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:16

# redis docker creation
docker run --name booking_redis-cache \
    -p 7379:6379 \
    --network=myNetwork \
    -d redis:7.4

# docker back build
sudo docker build -t booking_image .

# stop container
sudo docker rm booking_back

# docker back run
docker run --name booking_back \
    -p 7777:8000 \
    --network=myNetwork \
    booking_image

# celery
docker run --name booking_celery_worker \
    --network=myNetwork \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO

# celery beat
docker run --name booking_celery_beat \
    --network=myNetwork \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B

# gitlab
git config user.name "nikita strelenko"
git config user.email "snezerocode@gmail.com"