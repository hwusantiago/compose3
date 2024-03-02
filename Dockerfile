FROM python:3.11-slim
EXPOSE 5000
WORKDIR /app
COPY . /app
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
ENV FLASK_APP=movies-mysql.py
CMD ["python3","-m","flask", "run","--host=0.0.0.0"]