FROM python:3.9.4

COPY . /code/

WORKDIR /code

RUN pip install -r requirements.txt


ENV PYTHONUNBUFFERED=1

# EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]