from restaurant import pastebin
from celery import shared_task


create_paste = shared_task(pastebin.create_paste)
