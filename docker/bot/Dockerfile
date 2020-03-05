FROM python:3.7.2
WORKDIR /usr/src/app
COPY ./bot .
RUN pip3 install --upgrade pip
RUN pip3 --version
RUN pip3 install aiogram
RUN pip3 install requests
RUN pip3 install bs4
RUN nohup python3 Bot.py &
# RUN pip install -r requirements.txt
