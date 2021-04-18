FROM python:3.6

ENV DockerHOME=/home/akshay/Desktop/IIITB/SPE_Speech_Evaluator

RUN mkdir -p $DockerHOME

WORKDIR $DockerHOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY . $DockerHOME 

RUN pip install -r requirements.txt

EXPOSE 8000

CMD python manage.py runserver

