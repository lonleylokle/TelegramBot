FROM nginx
COPY ./site /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
RUN cat /usr/share/nginx/html/index.html && cat /etc/nginx/nginx.conf 
COPY nginx.conf /etc/nginx/nginx.conf
RUN cat /etc/nginx/nginx.conf && mkdir /etc/nginx/ssl && apt-get update && apt-get install openssl && openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt -subj '/CN=mydom.com/O=My Company Name LTD./C=US'
