FROM python:3.7

RUN pip install -r requirements.txt
RUN source envvars.sh
 
RUN mkdir /app
ADD . /app
WORKDIR /app

CMD python /app/bot/bot.py
