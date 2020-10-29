# restaurant

This is a test project for OOO "Kirpich".


## Deploy (development)

- Create and start containers with ```docker-compose up --build```
- Setup database
    - ```docker exec -it restaurant_db_1 bash```
        - ```su postgres```
        - ```psql```
        - ```CREATE DATABASE restaurant;```
        - ```Ctrl+d``` ```Ctrl+d``` ```Ctrl+d```
    - ```docker exec -it restaurant_web_1 bash```
        - ```python manage.py migrate```
        - ```python manage.py createsuperuser```
        - ```Ctrl+d```
- Stop containers with ```Ctrl+c```
- Start containers again with ```docker-compose start```
