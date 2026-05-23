# 03 - Zabbix 监控系统

## 知识点总结

### 核心概念
- **Zabbix**: 企业级开源监控解决方案
- **Zabbix Server**: 核心服务器，处理数据和告警
- **Zabbix Agent**: 安装在被监控主机上的代理
- **模板(Template)**: 预定义的监控项集合

### 架构
```
Zabbix Server (Docker) <--Agent--> client-web / client-db
       |
  Web界面 (80端口)
```

## 实操步骤

### 1. Docker Compose部署Zabbix Server

```yaml
# docker-compose.yml
version: '3.8'
services:
  zabbix-server:
    image: zabbix/zabbix-server-mysql:6.0-latest
    container_name: zabbix-server
    restart: always
    environment:
      DB_SERVER_HOST: mysql-server
      MYSQL_DATABASE: zabbix
      MYSQL_USER: zabbix
      MYSQL_PASSWORD: zabbix_pwd
      ZBX_CACHESIZE: 512M
    ports:
      - "10051:10051"
    networks:
      - zabbix-net

  zabbix-web:
    image: zabbix/zabbix-web-nginx-mysql:6.0-latest
    container_name: zabbix-web
    restart: always
    environment:
      DB_SERVER_HOST: mysql-server
      MYSQL_DATABASE: zabbix
      MYSQL_USER: zabbix
      MYSQL_PASSWORD: zabbix_pwd
      ZBX_SERVER_HOST: zabbix-server
    ports:
      - "80:8080"
    depends_on:
      - zabbix-server
    networks:
      - zabbix-net

  mysql-server:
    image: mysql:8.0
    container_name: mysql-server
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root_pwd
      MYSQL_DATABASE: zabbix
      MYSQL_USER: zabbix
      MYSQL_PASSWORD: zabbix_pwd
    networks:
      - zabbix-net

networks:
  zabbix-net:
    driver: bridge
```

```bash
# 启动
docker compose up -d

# 验证
docker compose ps
```

### 2. 访问Web界面

- 浏览器访问: `http://192.168.50.10`
- 默认账号: `Admin`
- 默认密码: `zabbix`

### 3. Ansible安装Zabbix Agent

```yaml
# install-zabbix-agent.yml
---
- name: Install Zabbix Agent on clients
  hosts: web,db
  become: yes
  tasks:
    - name: Install Zabbix repo
      yum:
        name: "https://repo.zabbix.com/zabbix/6.0/rhel/9/x86_64/zabbix-release-6.0-4.el9.noarch.rpm"
        state: present

    - name: Install Zabbix Agent
      dnf:
        name: zabbix-agent
        state: present

    - name: Configure Zabbix Agent
      lineinfile:
        path: /etc/zabbix/zabbix_agentd.conf
        regexp: '^Server='
        line: 'Server=192.168.50.10'

    - name: Start Zabbix Agent
      systemd:
        name: zabbix-agent
        state: started
        enabled: yes
```

### 4. 添加被监控主机

1. Web界面 → 配置 → 主机 → 创建主机
2. 主机名称: `client-web` / `client-db`
3. 群组: `Linux servers`
4. 接口: 添加Agent接口 `192.168.50.20` / `192.168.50.30`
5. 模板: 链接 `Template OS Linux by Zabbix agent active`

## 常见问题与排错

| 问题 | 原因 | 解决 |
|------|------|------|
| Web界面打不开 | 端口映射错误 | 确认80端口映射到容器8080 |
| Agent连接失败 | Server配置错误 | 检查`/etc/zabbix/zabbix_agentd.conf`的Server行 |
| 无监控数据 | 模板未链接 | 主机配置中添加Linux模板 |
| 容器启动失败 | 端口冲突 | `ss -tlnp` 检查端口占用 |

## 速记口诀

> **Docker三件套一键起，Admin/zabbix登录，Agent配Server IP，模板链接数据来。**
