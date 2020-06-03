FROM python:3.7.2
COPY ./bot ./bot
RUN pip3 install --upgrade pip
RUN pip3 --version
RUN pip3 install aiogram
RUN pip3 install requests
RUN pip3 install bs4
CMD ["python3.7","./bot/test_bot.py"]
