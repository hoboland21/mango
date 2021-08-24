FROM nginx

WORKDIR /usr/src/app/nginx

COPY  portal_mcsaipan_net.conf /etc/nginx/conf.d/
RUN rm /etc/nginx/conf.d/default.conf
ENV TZ=Pacific/Saipan
