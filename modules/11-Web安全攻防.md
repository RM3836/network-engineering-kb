# 11 - Web安全与攻防实战

## 知识点总结

### 核心概念
- **ARP欺骗**: 伪造ARP报文，劫持局域网流量（中间人攻击）
- **Windows口令破解**: 获取SAM表Hash值，离线破解
- **VBS病毒**: 基于VBScript的脚本型病毒
- **恶意代码分析**: 通过行为监控识别病毒特征

### 攻击类型概览

| 攻击类型 | 原理 | 防御 |
|----------|------|------|
| ARP欺骗 | 伪造MAC地址映射 | 静态ARP绑定、ARP防火墙 |
| 口令破解 | 暴力/字典/彩虹表 | 强密码、账号锁定、MFA |
| VBS病毒 | 脚本执行+自启动 | 禁用脚本、杀毒软件 |
| WebShell | JSP/PHP后门 | 文件完整性检查、WAF |

## 实操步骤

### 1. ARP欺骗攻击（Cain工具）

```bash
# 环境：3台Win2003虚拟机
# 攻击机: 192.168.1.2
# 目标机: 192.168.1.253 (被欺骗)
# 网关:   192.168.1.254

# 步骤:
# 1. 打开Cain → 配置嗅探器 → 扫描本网段MAC
# 2. ARP毒化 → 添加目标对（网关 ↔ 目标机）
# 3. 开始ARP欺骗 → 拦截中间流量
# 4. 可嗅探到目标机的HTTP登录密码等信息
```

### 2. Windows口令破解

```bash
# 方法1: GetHashes工具
cd C:\tools
GetHashes.exe $local
# 获取SAM表中的NTLM Hash值

# 方法2: 系统命令绕过杀软
certutil -hashfile 文件名 MD5
certutil -hashfile 文件名 SHA256

# 方法3: PowerShell
Get-FileHash 文件名 -Algorithm MD5
```

### 3. VBS病毒编写与分析

```vbs
' 病毒核心行为:
' 1. 隐藏窗口 (Visible = False)
' 2. 锁定任务管理器 (Open taskmgr.exe Lock Read)
' 3. 循环弹窗骚扰 (MsgBox)
' 4. 打开恶意网站 (Shell "explorer.exe http://xxx")
' 5. 写入垃圾文件到磁盘

' 防御要点:
' - 禁用Windows Script Host
' - 安装杀毒软件实时监控
' - 不运行来源不明的脚本
```

### 4. Linux入侵痕迹排查

```bash
# 查看当前登录用户
who

# 锁定可疑用户
passwd -l suspicious_user

# 踢掉可疑用户
ps -ef | grep @pts/1
kill -9 <PID>

# 查看登录历史
last

# 查找WebShell
find . -type f -name "*.jsp" | xargs grep -i "getRuntime"
find . -type f -name "*.jsp" | xargs grep -i "jspspy"

# 检查认证日志
cat /var/log/auth.log

# 查找可疑ELF文件
find / -name "*.elf" | xargs ls -l
```

### 5. 文件系统加固

```bash
# 锁定关键文件（immutable）
chattr +i /etc/passwd /etc/shadow /etc/hosts

# 日志文件只追加
chattr +a /var/log/messages /var/log/secure

# 查找SUID程序（提权风险）
find / -type f -perm -4000 -print

# 查找任意用户可写文件
find / -type f -perm -2 -o -perm -20 | xargs ls -al
```

## 常见问题与排错

| 问题 | 原因 | 解决 |
|------|------|------|
| ARP欺骗不生效 | 网卡混杂模式未开 | Cain中启用Sniffer |
| Hash破解太慢 | 字典太小 | 使用rainbow table |
| chattr +i后无法修改 | 需要先解除 | `chattr -i 文件名` |
| kill用户后仍在线 | 多终端登录 | `who`检查所有终端 |

## 速记口诀

> **ARP欺骗劫流量，GetHashes拿口令，VBS隐藏锁任务管，chattr加i锁文件。**
