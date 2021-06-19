FROM python:alpine

RUN apk add --update --no-cache --virtual  .build-deps  build-base gammu-dev pkgconfig &&\
    pip3 install --upgrade pika requests aiogram python-gammu&&\
    apk del .build-deps &&\
    apk add --update gammu-smsd supervisor

CMD [ "/usr/bin/supervisord", "-c", "/etc/supervisord.conf" ]