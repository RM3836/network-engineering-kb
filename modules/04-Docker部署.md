# 04 - Docker 应用部署

## 知识点总结

### 核心概念
- **动静分离**: Nginx处理静态资源，Tomcat处理动态请求
- **Docker Compose**: 多容器编排工具
- **数据卷挂载**: 容器数据持久化到宿主机
- **端口映射**: 容器端口暴露到宿主机

### 架构
```
客户端 --> Nginx(80) --> 静态资源(/data/static)
         --> Tomcat(8080) --> 动态资源(/data/tomcat/webapps)

client-db --> MySQL(3306) --> /data/mysql_data
```

## 实操步骤

### 1. 客户机1：Nginx + Tomcat 动静分离

```bash
# 创建目录
mkdir -p /data/static /data/tomcat/webapps

# 创建测试静态页面
echo "<h1>Hello from Nginx Static!</h1>" > /data/static/index.html
```

```yaml
# docker-compose.yml (client-web)
version: '3.8'
services:
  nginx:
    image: nginx:latest
    container_name: nginx-proxy
    restart: always
    ports:
      - "80:80"
    volumes:
      - /data/static:/usr/share/nginx/html:ro
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - tomcat
    networks:
      - web-net

  tomcat:
    image: tomcat:9.0-jdk17
    container_name: tomcat-app
    restart: always
    ports:
      - "8080:8080"
    volumes:
      - /data/tomcat/webapps:/usr/local/tomcat/webapps
    networks:
      - web-net

networks:
  web-net:
    driver: bridge
```

```nginx
# nginx.conf
server {
    listen 80;
    server_name localhost;

    # 静态资源
    location / {
        root /usr/share/nginx/html;
        index index.html;
    }

    # 动态请求转发Tomcat
    location /app/ {
        proxy_pass http://tomcat:8080/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# 启动
docker compose up -d

# 验证
curl http://localhost          # 静态页面
curl http://localhost:8080     # Tomcat默认页
```

### 2. 客户机2：MySQL 单实例

```bash
# 创建数据目录
mkdir -p /data/mysql_data

# 部署MySQL
docker run -d \
  --name mysql-single \
  --restart always \
  -e MYSQL_ROOT_PASSWORD=dbpassword \
  -v /data/mysql_data:/var/lib/mysql \
  -p 3306:3306 \
  mysql:8.0

# 验证连接
docker exec -it mysql-single mysql -u root -pdbpassword -e "SELECT 1;"
```

### 3. 本地连接MySQL

```bash
# 安装mysql客户端
sudo dnf install -y mysql

# 连接测试
mysql -h 192.168.50.30 -u root -pdbpassword
```

## 常见问题与排错

| 问题 | 原因 | 解决 |
|------|------|------|
| Nginx返回403 | 挂载目录为空 | 确认`/data/static`下有index.html |
| Tomcat访问不了 | 容器未就绪 | `docker logs tomcat-app`查看日志 |
| MySQL连接拒绝 | 端口未映射 | 确认`-p 3306:3306` |
| 数据丢失 | 未挂载卷 | 确认`-v /data/mysql_data:/var/lib/mysql` |

## 速记口诀

> **Nginx静态Tomcat动，compose编排卷挂载，MySQL单机dbpassword，端口映射要确认。**
