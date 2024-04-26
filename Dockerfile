FROM python:3-alpine3.12

WORKDIR /app

COPY . /app 

RUN pip install -r requirements.txt
RUN pip install -U python-dotenv

CMD ["python", "./src/app.py"]