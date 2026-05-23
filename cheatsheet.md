# 网络工程速查表 (Cheatsheet)

> 一页纸浓缩所有常用命令，考试/面试前快速回顾用。

---

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
```

## 二、Ansible

```bash
dnf install -y ansible
ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa
ssh-copy-id root@192.168.50.20
ansible all -m ping
ansible-playbook install-nginx.yml
```

## 三、Zabbix

```bash
docker compose up -d                    # 启动Zabbix三件套
# 访问: http://192.168.50.10 (Admin / zabbix)
dnf install -y zabbix-agent             # 安装Agent
# 配置: Server=192.168.50.10
systemctl enable --now zabbix-agent
```

## 四、Docker基础

```bash
docker compose up -d                    # Nginx+Tomcat动静分离
docker run -d --name mysql-single --restart always \
  -e MYSQL_ROOT_PASSWORD=dbpassword \
  -v /data/mysql_data:/var/lib/mysql \
  -p 3306:3306 mysql:8.0
mysql -h 192.168.50.30 -u root -pdbpassword
```

## 五、Docker进阶

```bash
docker build -t my-app:v1 .            # 构建镜像
docker run -d --name web -p 80:80 my-app:v1
docker exec -it web bash               # 进入容器
docker logs -f web                      # 查看日志
docker push username/my-app:v1         # 推送镜像
docker system prune -a                 # 清理空间
```

## 六、VMware虚拟化

```bash
# ESXi: https://<IP>:9443 (root)
# vCenter: https://<IP>:443 (administrator@vsphere.local)
# 关键功能: vMotion(在线迁移) HA(高可用) DRS(负载均衡)
# 存储: SSD(高性能) + SAS(大容量), Round Robin多路径
# 网络: vDS分布式交换机 + VLAN隔离
```

## 七、防火墙

```bash
# 安全区域: Trust / Untrust / DMZ
# NAT: 私有IP → 公有IP（节省地址）
# HRP: 主备状态同步（双机热备）
# 智能选路: 链路质量负载分担
# 状态检测: 跟踪连接状态，动态放行返回流量
```

## 八、Linux攻防

```bash
john /tmp/password.db                  # 口令破解
chattr +i /etc/passwd /etc/shadow      # 文件加固
chattr +a /var/log/messages            # 日志只追加
find / -type f -perm -4000 -print      # 查找SUID
who && last                            # 登录检查
passwd -l suspicious_user              # 锁定用户
```

## 九、Web安全

```bash
# ARP欺骗: Cain工具 → ARP毒化 → 流量劫持
# 口令破解: GetHashes.exe $local → 获取SAM Hash
# VBS病毒: 隐藏窗口 + 锁任务管理器 + 弹窗 + 写垃圾文件
# 入侵排查: who/last/auth.log + find JSP WebShell
# 防御: chattr锁文件 + SSH密钥 + MFA
```

## 十、WLAN无线网络

```bash
# Wi-Fi 6 = 802.11ax, 9.6Gbps
# 关键技术: OFDMA(多用户) 1024-QAM TWT(省电) BSS Color
# CAPWAP: 控制(UDP 5246) + 数据(UDP 5247)
# WPA3-SAE: 防暴力破解
# RTS/CTS: 解决隐藏节点
# 漫游: 切换<50ms
```

## 十一、网络爬虫

```python
import requests, pandas as pd, time, random
# 微博API: https://m.weibo.cn/api/container/getIndex
# 反爬: Cookie + User-Agent + 随机延迟(1-3s)
# 数据: requests.get() → json → pandas DataFrame → CSV
# 可视化: jieba分词 → WordCloud词云
```

## 十二、常用排错命令

```bash
# 网络
ip addr show                    # 查看IP
ping -c 3 <目标IP>              # 测试连通性
ss -tlnp                        # 查看监听端口
nmcli device                    # 查看网卡状态

# Docker
docker ps -a                    # 查看所有容器
docker logs <容器名>             # 查看日志
docker compose ps               # 编排服务状态
docker stats                    # 资源使用

# 系统
systemctl status <服务名>        # 查看服务状态
journalctl -u <服务名> -f        # 实时日志
df -h                           # 磁盘使用
free -h                         # 内存使用
```

## 十三、虚拟化方案设计要点

```
需求分析 → 量化指标(VM数/SLA/性能)
架构设计 → 分层拓扑(物理/虚拟/网络/存储)
计算设计 → 集群+HA+DRS+亲和性
存储设计 → FC/iSCSI/NFS/vSAN + SSD/SAS分层
网络设计 → vDS + VLAN隔离(管理/vMotion/存储/业务)
权限设计 → RBAC角色(管理员/VM管理员/只读)
```
