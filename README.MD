# Xianju-chat-service

## Introduction

This is a module of xianju server, maintaining app's chat services. i.e. simple authorization system(not used in app), API and ez WebUI.



## Deployment

### Docker

(NOT implemented yet)

### Manually

Do as following step to run service on you local machine.

1. Clone this repository

2. Configure python venv

   running following commands in the directory you clone this repository

   ```powershell
   python -m venv venv
   ```

3. Install required packages

   ```powershell
   pip install -r requirements.txt
   ```

4. Tweak configurations

   You can set `config.py` and `.env` as you want.

   In most cases, you must configurate `DATABASE_BASE_URL`  in the `.env` file to the database currently running on your machine

5. Run

   To initialize database and fill it with some forgery data, you can run 

   ```powershell
   flask fill-db
   ```

   To clean database

   ```powershell
   flask clean-db
   ```

   run service

   ```powershell
   python chat-service.py
   ```

   

Now you can browse the webui: http://localhost:5000/webui. There is a easy demo of Socket.io implemented by javascript

The service also provide APIs, see API doc for more information: https://www.apifox.cn/apidoc/shared-75b228ec-c55b-4115-84c1-9dbcdb11ed5b

