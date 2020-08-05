FROM nginx
RUN cat /etc/nginx/nginx.conf
COPY ./docker/nginx/nginx.conf /etc/nginx/nginx.conf
RUN mkdir /etc/nginx/ssl
COPY ./docker/nginx/nginx.crt /etc/nginx/ssl/nginx.crt
COPY ./docker/nginx/nginx.key /etc/nginx/ssl/nginx.key
