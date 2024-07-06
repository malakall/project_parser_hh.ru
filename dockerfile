FROM python:3.9-slim



RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev build-essential \
    && apt-get clean

WORKDIR /app


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . .

# run com
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]