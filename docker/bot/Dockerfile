FROM python:3.7.2
COPY . .
COPY ./docker/nginx/nginx.crt .
COPY ./docker/nginx/nginx.key .
RUN pip3 install --upgrade pip
RUN pip3 --version
RUN pip3 install aiogram
RUN pip3 install requests
RUN pip3 install bs4
#RUN nohup python3 Bot.py
CMD ["python3","app.py"]
# RUN pip install -r requirements.txt
