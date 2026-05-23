# 05 - VMware vSphere 虚拟化

## 知识点总结

### 核心概念
- **ESXi**: VMware裸机虚拟化平台，直接安装在物理服务器上
- **vCenter (vCSA)**: 集中管理多台ESXi主机的管理平台
- **vMotion**: 虚拟机在线迁移（不停机）
- **HA (高可用)**: 主机故障时自动重启虚拟机
- **DRS**: 根据负载自动分配虚拟机

### 架构
```
vCenter (vCSA) ──管理──> ESXi主机1 ──> 虚拟机A、B
                  ├──管理──> ESXi主机2 ──> 虚拟机C、D
                  └──管理──> 共享存储(LUN)
```

## 实操步骤

### 1. 安装ESXi

```bash
# 1. 制作U盘启动盘（Rufus）
#    - 选择ESXi 8.0 ISO
#    - 分区类型: GPT
#    - 启动类型: UEFI

# 2. 裸机安装
#    - 开机F12选U盘启动
#    - 选择安装磁盘
#    - 设置root密码（大小写+数字+特殊，≥8位）

# 3. 配置管理网络
#    IP: 192.168.10.10
#    子网: 255.255.255.0
#    网关: 192.168.10.1
#    DNS: 223.5.5.5

# 4. 验证
#    浏览器访问 https://192.168.10.10:9443
#    账号: root / 密码: 你设置的密码
```

### 2. 部署vCenter (vCSA)

```
# 阶段1: 部署设备
1. 挂载vCenter Server 8.0镜像
2. 运行 vcsa-ui-installer/win32/installer.exe
3. 选择"安装" → "部署vCenter Server Appliance"
4. 目标ESXi: 192.168.10.10 + root密码
5. 设备名称: vCenter-01
6. 部署大小: 小型（≤10台ESXi）
7. 网络: IP 192.168.10.20, 子网 255.255.255.0

# 阶段2: 设置设备
1. NTP服务器: 192.168.10.1
2. SSO域名: vsphere.local
3. SSO密码: Sso@1234

# 验证
# 浏览器访问 https://192.168.10.20:443
# 账号: administrator@vsphere.local
```

### 3. 配置数据中心

```
vCenter管理界面:
1. 创建数据中心(Data Center)
2. 创建集群(Cluster)
3. 启用HA和DRS
4. 添加ESXi主机到集群
5. 配置存储（添加LUN）
6. 配置网络（vSwitch/VLAN）
```

### 4. 关键配置项

| 配置项 | 说明 |
|--------|------|
| vMotion | 虚拟机不停机迁移 |
| HA | 主机故障自动重启VM |
| DRS | 负载均衡自动调度 |
| Update Manager | 补丁集中管理 |
| Converter | P2V物理机转虚拟机 |

## 常见问题与排错

| 问题 | 原因 | 解决 |
|------|------|------|
| ESXi安装失败 | 未开启VT-x/AMD-V | BIOS中启用虚拟化 |
| vCSA部署超时 | DNS未配置 | 确保DNS可达 |
| 无法vMotion | 网络不通 | 检查vMotion端口组配置 |
| 存储不可见 | Zoning错误 | 检查SAN交换机Zone配置 |

## 速记口诀

> **ESXi裸机装U盘，vCSA两阶段部署，HA保可用DRS均衡，vMotion迁移不停机。**
