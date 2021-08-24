FROM nginx

WORKDIR /usr/src/app/nginx

COPY mango.conf /etc/nginx/conf.d/
RUN rm /etc/nginx/conf.d/default.conf
ENV TZ=Pacific/Saipan
