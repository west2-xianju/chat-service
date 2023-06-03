# Xianju-chat-service

## Introduction

This is a module of Xianju server, maintaining app's chat services. i.e. simple authorization system(not used in app), API and WebUI(xianju-admin-frontend).



## Deployment

### Docker

 Notice: Replace labels concluded with `<>` with custom content.

To deploy the Service using Docker, follow these steps:

1. Ensure that Docker is installed on your system. You can download Docker from the official website: [https://www.docker.com](https://www.docker.com).

2. Clone this repository to your local machine:

   ```shell
   git clone https://github.com/west2-xianju/chat-service
   ```

3. Navigate to the project directory:

   ```shell
   cd chat-service
   ```

4. Build the Docker image:

   ```shell
   docker build -t <custom-tag-name> .
   ```

5. Run the Docker container:

   ```shell
   docker run -p <outside-port>:5000 <custom-tag-name>
   ```

   The backend service will now be running on `http://localhost:<outside-port>`.

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

   

There is an implemented page in xianju-admin-frontend repo. 

The service also provide APIs, see API doc for more information: https://www.apifox.cn/apidoc/shared-75b228ec-c55b-4115-84c1-9dbcdb11ed5b

