from django.core.management.utils import get_random_secret_key, get_random_string

rabbit_password = get_random_string(20)

secrets = {
    "POSTGRES_USER": "postgres",
    "POSTGRES_PASSWORD": "postgres",

    "RABBITMQ_ERLANG_COOKIE": get_random_string(50),
    "RABBITMQ_DEFAULT_USER": "guest",
    "RABBITMQ_DEFAULT_PASS": rabbit_password,

    "SECRET_KEY": get_random_secret_key(),
    "DATABASE_URL": "postgres://postgres:postgres@db:5432/restaurant",
    "CELERY_BROKER_URL": f"pyamqp://guest:{rabbit_password}@rabbitmq//",
    "API_TOKEN": get_random_string(40),
    "PASTEBIN_API_DEV_KEY": "<get your own on pastebin.com>",
}

for k, v in secrets.items():
    print(f"{k}={v}")
