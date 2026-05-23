# 02 - Ansible 自动化部署

## 知识点总结

### 核心概念
- **Ansible**: 无Agent的自动化运维工具，通过SSH连接管理节点
- **主机清单(Inventory)**: 定义被管理节点的文件
- **Playbook**: YAML格式的自动化任务脚本
- **幂等性**: 同一Playbook执行多次，结果一致

### 架构
```
控制节点(server-node) --SSH--> 客户机(client-web, client-db)
```

## 实操步骤

### 1. 安装Ansible（控制节点）

```bash
# CentOS Stream 9 默认源安装
sudo dnf install -y ansible

# 验证
ansible --version
```

### 2. 配置SSH免密登录

```bash
# 在server-node上生成密钥对
ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa

# 分发公钥到两台客户机
ssh-copy-id root@192.168.50.20
ssh-copy-id root@192.168.50.30

# 验证免密登录
ssh root@192.168.50.20 "hostname"
ssh root@192.168.50.30 "hostname"
```

### 3. 编写主机清单

```ini
# /etc/ansible/hosts
[web]
client-web ansible_host=192.168.50.20

[db]
client-db ansible_host=192.168.50.30

[all:vars]
ansible_user=root
ansible_ssh_private_key_file=~/.ssh/id_rsa
```

### 4. 测试连通性

```bash
ansible all -m ping
```

预期输出：
```
client-web | SUCCESS => {"changed": false, "ping": "pong"}
client-db | SUCCESS => {"changed": false, "ping": "pong"}
```

### 5. 编写Playbook安装Nginx

```yaml
# install-nginx.yml
---
- name: Install and start Nginx on clients
  hosts: web,db
  become: yes
  tasks:
    - name: Install Nginx
      dnf:
        name: nginx
        state: present

    - name: Start and enable Nginx
      systemd:
        name: nginx
        state: started
        enabled: yes
```

### 6. 执行Playbook

```bash
ansible-playbook install-nginx.yml

# 验证Nginx版本（在客户机上）
nginx -v
```

## 常见问题与排错

| 问题 | 原因 | 解决 |
|------|------|------|
| SSH连接拒绝 | 未安装openssh-server | `dnf install opensh-server` |
| 免密登录失败 | 权限问题 | `chmod 700 ~/.ssh; chmod 600 ~/.ssh/authorized_keys` |
| Playbook语法错误 | YAML缩进 | 确保2空格缩进，不要用Tab |
| ping返回FAILED | 防火墙/SELinux | 确保已关闭（模块01） |

## 速记口诀

> **装Ansible分公钥，hosts分组写清单，Playbook YAML两空格，ping通再跑任务。**
