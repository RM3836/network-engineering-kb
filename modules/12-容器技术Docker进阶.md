# 12 - 容器技术 (Docker 进阶)

## 知识点总结

### 核心概念
- **Docker**: 容器化平台，轻量级虚拟化替代方案
- **Dockerfile**: 定义镜像构建过程的脚本文件
- **镜像(Image)**: 只读模板，包含运行应用所需的一切
- **容器(Container)**: 镜像的运行实例
- **注册中心(Registry)**: 存储和分发镜像的服务

### Docker vs 虚拟机

| 特性 | Docker容器 | 虚拟机 |
|------|-----------|--------|
| 启动速度 | 秒级 | 分钟级 |
| 资源占用 | MB级 | GB级 |
| 隔离级别 | 进程级 | 系统级 |
| 性能损耗 | ~0% | 5-15% |
| 镜像大小 | 通常<500MB | 通常>5GB |

## 实操步骤

### 1. Docker环境搭建

```bash
# 安装Docker
sudo dnf install -y docker-ce docker-ce-cli containerd.io
sudo systemctl enable --now docker

# 配置镜像加速（国内网络）
sudo mkdir -p /etc/docker
cat > /etc/docker/daemon.json << 'EOF'
{
  "registry-mirrors": ["https://mirror.ccs.tencentyun.com"]
}
EOF
sudo systemctl restart docker

# 验证
docker run hello-world
docker info
```

### 2. Dockerfile构建镜像

```dockerfile
# Dockerfile示例：构建Nginx自定义镜像
FROM nginx:latest

# 维护者信息
LABEL maintainer="YURM <steam3836@foxmail.com>"

# 复制自定义配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 复制静态文件
COPY html/ /usr/share/nginx/html/

# 暴露端口
EXPOSE 80

# 启动命令
CMD ["nginx", "-g", "daemon off;"]
```

```bash
# 构建镜像
docker build -t my-nginx:v1 .

# 运行容器
docker run -d --name my-web -p 80:80 my-nginx:v1

# 查看镜像层
docker history my-nginx:v1
```

### 3. 注册中心使用

```bash
# 登录Docker Hub
docker login

# 打标签
docker tag my-nginx:v1 username/my-nginx:v1

# 推送镜像
docker push username/my-nginx:v1

# 拉取镜像
docker pull username/my-nginx:v1

# 私有注册中心
docker login registry.example.com
docker tag my-nginx:v1 registry.example.com/my-nginx:v1
docker push registry.example.com/my-nginx:v1
```

### 4. 常用Docker命令

```bash
# 镜像管理
docker images                    # 列出镜像
docker rmi <镜像名>              # 删除镜像
docker image prune               # 清理无用镜像

# 容器管理
docker ps                        # 运行中的容器
docker ps -a                     # 所有容器
docker stop/start/restart <容器>  # 生命周期
docker exec -it <容器> bash      # 进入容器
docker logs -f <容器>            # 查看日志
docker stats                     # 资源使用

# 网络
docker network ls                # 列出网络
docker network create my-net     # 创建网络
docker run --network my-net ...  # 指定网络

# 数据卷
docker volume create my-data     # 创建卷
docker run -v my-data:/app ...   # 挂载卷
```

## Dockerfile最佳实践

```dockerfile
# 1. 使用多阶段构建减小镜像
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN go build -o main .

FROM alpine:latest
COPY --from=builder /app/main /main
CMD ["/main"]

# 2. 合并RUN减少层数
RUN apt-get update && \
    apt-get install -y curl wget && \
    rm -rf /var/lib/apt/lists/*

# 3. 使用.dockerignore排除不需要的文件
# .git, node_modules, *.log

# 4. 不要在镜像中存储密钥
# 使用环境变量或挂载文件
```

## 常见问题与排错

| 问题 | 原因 | 解决 |
|------|------|------|
| 容器立即退出 | 主进程结束 | 检查CMD是否前台运行 |
| 镜像构建慢 | 未利用缓存 | 把不常变的层放前面 |
| 磁盘空间不足 | 旧镜像堆积 | `docker system prune -a` |
| 容器间不通 | 不在同一网络 | `docker network connect` |

## 速记口诀

> **Dockerfile定义镜像，build构建run运行，registry推送pull拉取，volume持久network通。**
