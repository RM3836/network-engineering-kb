# 网络工程知识库

> 从大学四年课程作业中提炼的结构化知识库，涵盖运维、虚拟化、安全、无线、容器、爬虫六大领域。

## 知识地图

```
网络工程知识库
├── 运维自动化
│   ├── 01-环境准备与虚拟机配置
│   ├── 02-Ansible自动化部署
│   ├── 03-Zabbix监控系统
│   └── 04-Docker应用部署
├── 虚拟化技术
│   ├── 05-VMware-vSphere虚拟化
│   ├── 09-VMware企业架构设计
│   └── 13-虚拟化考核方案
├── 网络安全
│   ├── 06-防火墙技术
│   ├── 07-Linux攻防实战
│   └── 11-Web安全攻防
├── 无线网络
│   └── 08-WLAN无线网络技术
├── 容器技术
│   └── 12-容器技术Docker进阶
└── 网络爬虫
    └── 10-网络爬虫技术
```

## 模块列表

| # | 模块 | 文件 | 关键技术 | 来源课程 |
|---|------|------|----------|----------|
| 01 | 环境准备 | [modules/01-环境准备.md](modules/01-环境准备.md) | CentOS, 双网卡, Docker | 网络运维 |
| 02 | Ansible | [modules/02-Ansible自动化.md](modules/02-Ansible自动化.md) | SSH免密, Playbook | 网络运维 |
| 03 | Zabbix | [modules/03-Zabbix监控.md](modules/03-Zabbix监控.md) | Docker Compose, Agent | 网络运维 |
| 04 | Docker部署 | [modules/04-Docker部署.md](modules/04-Docker部署.md) | Nginx+Tomcat, MySQL | 网络运维 |
| 05 | VMware基础 | [modules/05-VMware虚拟化.md](modules/05-VMware虚拟化.md) | ESXi, vCenter, vCSA | 虚拟化技术 |
| 06 | 防火墙 | [modules/06-防火墙技术.md](modules/06-防火墙技术.md) | NAT, HRP, 双机热备 | 防火墙 |
| 07 | Linux攻防 | [modules/07-Linux攻防.md](modules/07-Linux攻防.md) | John破解, chattr, 入侵排查 | 网络安全 |
| 08 | WLAN | [modules/08-WLAN无线网络.md](modules/08-WLAN无线网络.md) | Wi-Fi 6, CAPWAP, OFDMA | 无线网络 |
| 09 | VMware架构 | [modules/09-VMware企业架构设计.md](modules/09-VMware企业架构设计.md) | 分层架构, 存储分层, RBAC | 虚拟化技术 |
| 10 | 网络爬虫 | [modules/10-网络爬虫技术.md](modules/10-网络爬虫技术.md) | requests, pandas, 词云 | 网络爬虫技术 |
| 11 | Web安全 | [modules/11-Web安全攻防.md](modules/11-Web安全攻防.md) | ARP欺骗, VBS病毒, WebShell | 网络安全 |
| 12 | Docker进阶 | [modules/12-容器技术Docker进阶.md](modules/12-容器技术Docker进阶.md) | Dockerfile, Registry | 容器技术 |
| 13 | 虚拟化考核 | [modules/13-虚拟化考核方案.md](modules/13-虚拟化考核方案.md) | 方案设计, 预算, 实施 | 虚拟化技术 |

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/RM3836/network-engineering-kb.git
cd network-engineering-kb

# 查看速查表
cat cheatsheet.md

# 使用自动化脚本
cd scripts/
bash setup-env.sh server-node 192.168.50.10
bash install-docker.sh
ansible-playbook -i hosts site.yml
```

## 速查表

👉 [cheatsheet.md](cheatsheet.md) — 一页纸浓缩所有常用命令

## 脚本目录

| 脚本 | 用途 |
|------|------|
| [scripts/setup-env.sh](scripts/setup-env.sh) | 环境初始化（关闭防火墙、配置网卡） |
| [scripts/install-docker.sh](scripts/install-docker.sh) | Docker 安装与启动 |
| [scripts/ansible-setup.yml](scripts/ansible-setup.yml) | Ansible 主机清单 + Playbook |
| [scripts/docker-compose-zabbix.yml](scripts/docker-compose-zabbix.yml) | Zabbix 一键部署 |
| [scripts/docker-compose-web.yml](scripts/docker-compose-web.yml) | Nginx+Tomcat 动静分离 |
| [scripts/nginx.conf](scripts/nginx.conf) | Nginx 动静分离配置 |
| [scripts/setup-mysql.sh](scripts/setup-mysql.sh) | MySQL 单实例部署 |

## 课程覆盖

- **网络管理与系统运维** — 模块 01-04
- **虚拟化技术** — 模块 05, 09, 13
- **防火墙技术** — 模块 06
- **网络安全/Linux攻防** — 模块 07, 11
- **无线网络技术** — 模块 08
- **网络爬虫技术** — 模块 10
- **容器技术** — 模块 12

---

**作者**: YURM (RM3836)
**学校**: 广州应用科技学院 · 网络工程专业
**GitHub**: https://github.com/RM3836
