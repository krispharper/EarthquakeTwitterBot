FROM python:3

RUN pip install requests tweepy
RUN mkdir /app
COPY bot.py /app/bot.py
WORKDIR /app

CMD ["python", "-u", "bot.py"]
