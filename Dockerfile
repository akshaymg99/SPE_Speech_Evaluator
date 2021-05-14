FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    python3.6 \
    python3-pip

RUN mkdir /SPE_Speech_Evaluator 

WORKDIR /SPE_Speech_Evaluator

COPY . /SPE_Speech_Evaluator

RUN apt-get -y install locales
RUN touch /usr/share/locale/locale.alias
ENV LANG=en_US.UTF-8 \ LANGUAGE=en_US \ LC_ALL=en_US.UTF-8

RUN echo $LANG
RUN python3 -c 'import locale; print(locale.getpreferredencoding())'

RUN apt-get update \
        && apt-get install -y pulseaudio alsa-utils alsa-base ffmpeg 

RUN apt-get update \
        && apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev libsndfile1-dev -y \
        && pip3 install pyaudio

RUN apt-get install -y pulseaudio

CMD python3 -c "import pyaudio"

COPY requirements.txt /SPE_Speech_Evaluator

RUN pip3 install django-elasticsearch-dsl
RUN pip3 install python-logstash

RUN pip3 install -r requirements.txt

COPY . /SPE_Speech_Evaluator

EXPOSE 8000

CMD python3 manage.py runserver 0.0.0.0:8000


