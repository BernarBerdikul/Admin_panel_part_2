
##Проверка проекта

1. Переименовать ```movies_admin/envs/*.env.example``` файлы на ```movies_admin/envs/*.env```

* оставил свои переменные

2. Запустить сборку контейнеров 
    ```
    docker-compose build
    docker-compose up
    ```
3. Внутри контейнера **postgres_db** запустить backup базы 
   (для проверки лежит по пути ```movies_admin/docker/postgres/```)
    ```
    docker exec -it postgres_db sh
    pg_restore -U movies -d movies -v file.backup
    exit
    ```
