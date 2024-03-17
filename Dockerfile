FROM python:3.11.3

WORKDIR /app

COPY app .

RUN pip install flask

EXPOSE 5000

CMD ["python", "app.py"]
