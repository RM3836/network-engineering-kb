# 网络工程速查表 (Cheatsheet)

## 一、环境准备

```bash
# 关闭防火墙
systemctl stop firewalld && systemctl disable firewalld

# 关闭SELinux
setenforce 0 && sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config

# 配置静态IP（仅主机网卡）
nmcli connection modify ens224 ipv4.addresses 192.168.50.10/24 ipv4.method manual
nmcli connection up ens224

# 设置主机名
hostnamectl set-hostname server-node
echo "192.168.50.10 server-node" >> /etc/hosts

# 安装Docker
dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
systemctl enable --now docker
```

## 二、Ansible

```bash
# 安装
dnf install -y ansible

# SSH免密
ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa
ssh-copy-id root@192.168.50.20

# 测试连通性
ansible all -m ping

# 运行Playbook
ansible-playbook install-nginx.yml

# 主机清单格式 (/etc/ansible/hosts)
[web]
client-web ansible_host=192.168.50.20
```

## 三、Zabbix

```bash
# Docker部署Zabbix
docker compose up -d

# 访问: http://192.168.50.10
# 账号: Admin / zabbix

# Agent安装
dnf install -y zabbix-agent
# 配置 /etc/zabbix/zabbix_agentd.conf: Server=192.168.50.10
systemctl enable --now zabbix-agent
```

## 四、Docker

```bash
# Nginx + Tomcat 动静分离
docker compose up -d
curl http://localhost        # 静态
curl http://localhost:8080   # 动态

# MySQL单实例
docker run -d --name mysql-single --restart always \
  -e MYSQL_ROOT_PASSWORD=dbpassword \
  -v /data/mysql_data:/var/lib/mysql \
  -p 3306:3306 mysql:8.0

# 连接MySQL
mysql -h 192.168.50.30 -u root -pdbpassword
```

## 五、VMware虚拟化

```bash
# ESXi管理界面: https://192.168.10.10:9443
# vCenter管理: https://192.168.10.20:443
# 账号: administrator@vsphere.local

# 关键功能
# vMotion: 在线迁移VM
# HA: 主机故障自动重启VM
# DRS: 负载均衡自动调度
```

## 六、防火墙

```bash
# 安全区域: Trust / Untrust / DMZ
# NAT: 私有IP → 公有IP（节省地址）
# HRP: 主备状态同步（双机热备）
# 智能选路: 链路质量负载分担（优先走质量最好的）
```

## 七、Linux攻防

```bash
# 口令破解
john /tmp/password.db

# 文件加固
chattr +i /etc/passwd /etc/shadow
chattr +a /var/log/messages

# 安全检查
find / -type f -perm -4000 -print        # SUID文件
find / -nouser -o -nogroup               # 孤儿文件
who                                        # 当前登录
last                                       # 登录历史
passwd -l suspicious_user                 # 锁定用户
```

## 八、WLAN无线网络

```bash
# Wi-Fi标准
# Wi-Fi 6 = 802.11ax, 9.6Gbps, OFDMA, 1024-QAM, TWT
# CAPWAP隧道: 控制(UDP 5246) + 数据(UDP 5247)
# WPA3-SAE: 防暴力破解
# OFDMA: 多用户并行子载波
# RTS/CTS: 解决隐藏节点问题
# 漫游: 切换时延<50ms
```

## 九、常用排错命令

```bash
# 网络
ip addr show                    # 查看IP
ping -c 3 <目标IP>              # 测试连通性
ss -tlnp                        # 查看监听端口
nmcli device                    # 查看网卡状态

# Docker
docker ps -a                    # 查看所有容器
docker logs <容器名>             # 查看日志
docker compose ps               # 查看编排服务状态

# 系统
systemctl status <服务名>        # 查看服务状态
journalctl -u <服务名> -f        # 实时日志
df -h                           # 磁盘使用
free -h                         # 内存使用
```
