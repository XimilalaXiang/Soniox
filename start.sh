#!/bin/bash

set -euo pipefail

# Soniox 实时转录平台启动脚本

echo "🚀 启动 Soniox 实时转录平台..."

# 检查 Docker CLI 是否可用
if ! docker --version >/dev/null 2>&1; then
    echo "❌ 错误: Docker 未安装"
    echo "请访问 https://docs.docker.com/get-docker/ 安装 Docker"
    exit 1
fi

# 兼容 docker-compose (v1) 与 docker compose (v2)
if docker compose version >/dev/null 2>&1; then
    COMPOSE_CMD=(docker compose)
elif docker-compose version >/dev/null 2>&1; then
    COMPOSE_CMD=(docker-compose)
else
    echo "❌ 错误: Docker Compose 未安装"
    echo "请安装 Docker Compose v2（推荐）或 docker-compose"
    exit 1
fi

COMPOSE_DISPLAY="${COMPOSE_CMD[*]}"
IMAGE_TAG="${SONIOX_IMAGE_TAG:-latest}"

echo "🏷️  镜像标签: ${IMAGE_TAG}"

echo "🔍 检查 Compose 配置..."
if ! "${COMPOSE_CMD[@]}" config >/dev/null 2>&1; then
    echo "❌ Compose 配置校验失败。请在项目根目录创建 .env 并设置 SECRET_KEY。"
    echo "示例: SECRET_KEY=replace-with-a-random-secret"
    "${COMPOSE_CMD[@]}" config || true
    exit 1
fi

# 停止旧容器
echo "🛑 停止旧容器..."
"${COMPOSE_CMD[@]}" down

# 拉取最新镜像并启动服务
echo "📦 拉取最新镜像..."
"${COMPOSE_CMD[@]}" pull

echo "🔨 启动服务..."
"${COMPOSE_CMD[@]}" up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 5

# 检查服务状态
echo "📊 检查服务状态..."
"${COMPOSE_CMD[@]}" ps

echo ""
echo "✅ 启动完成！"
echo ""
echo "📱 访问地址："
echo "   - 前端: http://localhost:10081"
echo "   - 后端 API: 由前端反向代理到 /api (容器内地址 backend:8000)"
echo ""
echo "📝 查看日志："
echo "   ${COMPOSE_DISPLAY} logs -f backend"
echo "   ${COMPOSE_DISPLAY} logs -f frontend"
echo ""
echo "🛑 停止服务："
echo "   ${COMPOSE_DISPLAY} down"
