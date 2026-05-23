#!/bin/bash
# 环境初始化脚本 - 关闭防火墙、配置网络
# 用法: sudo bash setup-env.sh <hostname> <ip>
# 示例: sudo bash setup-env.sh server-node 192.168.50.10

HOSTNAME=${1:-"server-node"}
IP=${2:-"192.168.50.10"}

echo "========== 关闭防火墙 =========="
systemctl stop firewalld
systemctl disable firewalld
echo "[OK] 防火墙已关闭"

echo "========== 关闭SELinux =========="
setenforce 0
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
echo "[OK] SELinux已关闭"

echo "========== 设置主机名 =========="
hostnamectl set-hostname "$HOSTNAME"
echo "[OK] 主机名设置为: $HOSTNAME"

echo "========== 配置hosts =========="
grep -q "192.168.50.10 server-node" /etc/hosts || echo "192.168.50.10 server-node" >> /etc/hosts
grep -q "192.168.50.20 client-web" /etc/hosts || echo "192.168.50.20 client-web" >> /etc/hosts
grep -q "192.168.50.30 client-db" /etc/hosts || echo "192.168.50.30 client-db" >> /etc/hosts
echo "[OK] hosts已配置"

echo "========== 配置仅主机网卡 =========="
nmcli connection modify ens224 ipv4.addresses "${IP}/24" ipv4.method manual
nmcli connection up ens224
echo "[OK] 网卡IP设置为: $IP"

echo "========== 验证 =========="
echo "主机名: $(hostname)"
echo "IP地址: $(ip -4 addr show ens224 | grep inet | awk '{print $2}')"
echo "防火墙: $(systemctl is-active firewalld)"
echo "SELinux: $(getenforce)"
echo ""
echo "环境准备完成！"
