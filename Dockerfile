FROM python:latest


WORKDIR /usr/src/app
COPY req.txt ./
RUN pip install -r req.txt
COPY . .
RUN  python manage.py  makemigrations
RUN python manage.py  migrate
EXPOSE 80

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]