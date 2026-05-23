#!/bin/bash
# Docker安装脚本 - CentOS Stream 9
# 用法: sudo bash install-docker.sh

echo "========== 安装Docker =========="
dnf install -y dnf-plugins-core
dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

echo "========== 启动Docker =========="
systemctl start docker
systemctl enable docker

echo "========== 验证 =========="
systemctl status docker --no-pager
docker --version
docker compose version
echo ""
echo "Docker安装完成！"
