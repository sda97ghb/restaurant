# restaurant

This is a test project for OOO "Kirpich".


## Deploy (development)

- Create environment files with secrets. See usual .env files to determine keys. ```generate_secrets.py``` can help you.
    - ```db_secrets.env```
    - ```rabbitmq_secrets.env```
    - ```web_secrets.env```
        - ```DATABASE_URL``` must use username and password from ```db_secrets.env```
        - ```CELERY_BROKER_URL``` must use username and password from ```rabbitmq_secrets.env```
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
