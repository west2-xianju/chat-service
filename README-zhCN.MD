# Xianju-chat-service

## 简介

这是 闲橘 服务器的一个模块，用于维护应用的聊天服务，包括简单的授权系统（未在应用中使用）、API 和 WebUI（xianju-admin-frontend）。

## 功能特点

+ 通知功能：向在线/离线客户端推送通知。
+ 敏感消息检测：检查每条消息，自动过滤敏感词。
+ 离线消息持久化：将未投递的消息保存到数据库中，提供API以获取待接收的消息。
+ RESTful API：提供符合 RESTful 标准的API接口。

## 部署

### Docker

 注意: 将 `<>` 内的内容替换为自定义的内容

请按以下步骤使用 Docker 部署聊天服务：

1. 确保您的系统上已安装 Docker。您可以从官方网站下载 Docker：[https://www.docker.com](https://www.docker.com)。

2. 克隆此仓库到您的本地机器：

   ```shell
   git clone https://github.com/west2-xianju/chat-service
   ```

3. 进入项目目录：

   ```shell
   cd chat-service
   ```

4. 构建 Docker 镜像：

   ```shell
   docker build -t <自定义标签名> .
   ```

5. 运行 Docker 容器：

   ```shell
   docker run -p <外部端口>:5000 <自定义标签名>
   ```

   后端服务现在会在 `http://localhost:<外部端口>` 上运行。

### 手动部署

按照以下步骤在您的本地机器上运行服务。

1. 克隆此仓库。

2. 配置 Python 虚拟环境。

   在克隆的仓库目录中运行以下命令：

   ```powershell
   python -m venv venv
   ```

3. 安装所需的包。

   ```powershell
   pip install -r requirements.txt
   ```

4. 调整配置。

   您可以根据需要设置 `config.py` 和 `.env` 文件。

   在大多数情况下，您需要在 `.env` 文件中将 `DATABASE_BASE_URL` 配置为您正在运行的数据库的基本 URL。

5. 运行。

   若要初始化数据库并填充一些虚拟数据，可以运行以下命令：

   ```powershell
   flask fill-db
   ```

   若要清除数据库，请运行以下命令：

   ```powershell
   flask clean-db
   ```

   运行服务：

   ```powershell
   python chat-service.py
   ```

该服务在 xianju-admin-frontend 仓库中还有一个实现的页面。

该服务还提供了一组 API，详细信息请参阅 API 文档：https://www.apifox.cn/apidoc/shared-75b228ec-c55b-4115-84c1-9dbcdb11ed5b