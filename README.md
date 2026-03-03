# OpenSoniox 实时转录平台

基于 Soniox V4 的实时语音转录工具，支持发言人识别、历史记录与 AI 总结问答。

## 功能简介

- 实时语音转录（低延迟流式显示）
- 发言人识别（多说话人区分）
- 历史会话保存、搜索、导出（TXT/JSON/Markdown）
- AI 总结与问答（OpenAI 兼容接口）

## 部署方式

### 方式 1：使用 GHCR 预构建镜像（推荐，适合 1Panel）

镜像地址：

- 前端：`ghcr.io/ximilalaxiang/opensoniox-frontend:latest`
- 后端：`ghcr.io/ximilalaxiang/opensoniox-backend:latest`

可直接使用下面的 `compose`（把 `SECRET_KEY` 改成你自己的随机字符串）：

```yaml
services:
  backend:
    image: ghcr.io/ximilalaxiang/opensoniox-backend:latest
    container_name: opensoniox-backend
    restart: unless-stopped
    expose:
      - "17661"
    volumes:
      - /opt/opensoniox/data:/app/data
    environment:
      - PYTHONUNBUFFERED=1
      - DATABASE_URL=sqlite+aiosqlite:///./data/transcriptions.db
      - SECRET_KEY=replace-with-a-long-random-secret
      - ACCESS_PASSWORD=

  frontend:
    image: ghcr.io/ximilalaxiang/opensoniox-frontend:latest
    container_name: opensoniox-frontend
    restart: unless-stopped
    ports:
      - "17881:80"
    depends_on:
      - backend
```

启动：

```bash
docker compose pull
docker compose up -d
```

### 方式 2：本地源码构建后部署

```bash
git clone https://github.com/XimilalaXiang/OpenSoniox.git
cd OpenSoniox
docker compose -f docker-compose.dev.yml up -d --build
```

访问地址：`http://localhost:17881`

常用命令：

```bash
docker compose logs -f
docker compose down
```
