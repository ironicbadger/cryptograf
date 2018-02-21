FROM python:2.7

RUN mkdir /app
WORKDIR /app
ADD minerstat /app

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["python","/app/minerstat.py"]

