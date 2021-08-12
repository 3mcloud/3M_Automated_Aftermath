FROM python:3.9

RUN apt-get update && apt-get install -y \
    mdbtools

WORKDIR /app

COPY ./postgres_loader/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "src/main.py"]