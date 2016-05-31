FROM resin/rpi-raspbian:wheezy

MAINTAINER Joshua Parkin <joshuadparkin@gmail.com>

RUN sudo apt-get update 
RUN sudo apt-get install -y postgresql-9.1 
RUN apt-get -y install nginx  sed python-pip python-dev uwsgi-plugin-python supervisor

RUN mkdir -p /var/log/nginx/app/
RUN mkdir -p /var/log/uwsgi/app/

RUN rm /etc/nginx/sites-enabled/default
COPY flask.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf
COPY uwsgi.ini /var/www/app/
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

copy app /var/www/app
RUN sudo pip install -r ./requirements.txt

EXPOSE 80

CMD ["/usr/bin/supervisord"]