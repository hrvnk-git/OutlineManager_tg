# syntax=docker/dockerfile:1

FROM python:3.12-alpine
WORKDIR /outline_manager
COPY . /outline_manager
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "main.py"]