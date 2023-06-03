FROM python:3.11.0
WORKDIR /chat-api
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "chat-service.py"]
EXPOSE 5000