FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /opt/restaurant
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY manage.py ./
COPY restaurant_project restaurant_project/
COPY restaurant restaurant/
