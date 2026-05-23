# 网络工程知识库

> 从课程作业中提炼的实战知识，涵盖运维、虚拟化、安全、无线网络四大领域。

## 知识地图

```
网络工程知识库
├── 运维自动化
│   ├── 01-环境准备与虚拟机配置
│   ├── 02-Ansible自动化部署
│   ├── 03-Zabbix监控系统
│   └── 04-Docker应用部署
├── 虚拟化技术
│   └── 05-VMware-vSphere虚拟化
├── 网络安全
│   ├── 06-防火墙技术
│   └── 07-Linux攻防实战
└── 无线网络
    └── 08-WLAN无线网络技术
```

## 模块列表

| 模块 | 文件 | 关键技术 |
|------|------|----------|
| 环境准备 | [modules/01-环境准备.md](modules/01-环境准备.md) | CentOS Stream 9, 双网卡, Docker |
| Ansible | [modules/02-Ansible自动化.md](modules/02-Ansible自动化.md) | SSH免密, Playbook, 主机清单 |
| Zabbix | [modules/03-Zabbix监控.md](modules/03-Zabbix监控.md) | Docker Compose, Agent, 模板 |
| Docker | [modules/04-Docker部署.md](modules/04-Docker部署.md) | Nginx+Tomcat, MySQL, 动静分离 |
| VMware | [modules/05-VMware虚拟化.md](modules/05-VMware虚拟化.md) | ESXi, vCenter, vCSA |
| 防火墙 | [modules/06-防火墙技术.md](modules/06-防火墙技术.md) | NAT, HRP, 双机热备, 安全区域 |
| Linux攻防 | [modules/07-Linux攻防.md](modules/07-Linux攻防.md) | John破解, chattr, 入侵排查 |
| WLAN | [modules/08-WLAN无线网络.md](modules/08-WLAN无线网络.md) | Wi-Fi 6, CAPWAP, AC+AP |

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/RM3836/network-engineering-kb.git
cd network-engineering-kb

# 查看速查表
cat cheatsheet.md

# 使用 Ansible 自动化脚本
cd scripts/
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
| [scripts/setup-mysql.sh](scripts/setup-mysql.sh) | MySQL 单实例部署 |

---

**作者**: YURM (RM3836)  
**学校**: 广州应用科技学院 · 网络工程专业  
**课程**: 网络管理与系统运维 / 虚拟化技术 / 网络安全 / 无线网络技术
