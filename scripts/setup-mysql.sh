#!/bin/bash
# MySQL单实例部署脚本
# 用法: sudo bash setup-mysql.sh

echo "========== 创建数据目录 =========="
mkdir -p /data/mysql_data

echo "========== 部署MySQL容器 =========="
docker run -d \
  --name mysql-single \
  --restart always \
  -e MYSQL_ROOT_PASSWORD=dbpassword \
  -v /data/mysql_data:/var/lib/mysql \
  -p 3306:3306 \
  mysql:8.0

echo "========== 等待MySQL启动 =========="
sleep 10

echo "========== 验证连接 =========="
docker exec -it mysql-single mysql -u root -pdbpassword -e "SELECT VERSION();"

echo ""
echo "MySQL部署完成！"
echo "连接命令: mysql -h <IP> -u root -pdbpassword"
