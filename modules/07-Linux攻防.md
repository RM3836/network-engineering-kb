# 07 - Linux 攻防实战

## 知识点总结

### 核心概念
- **口令破解**: 使用John the Ripper等工具暴力破解密码
- **文件系统加固**: chattr命令锁定关键文件
- **入侵痕迹排查**: 检查登录日志、进程、木马文件
- **SUID/SGID**: 特殊权限位，可能被用于提权

## 实操步骤

### 1. 口令破解（John the Ripper）

```bash
# 安装John
sudo dnf install -y john

# 使用shadow文件破解
unshadow /etc/passwd /etc/shadow > /tmp/password.db
john /tmp/password.db

# 查看破解结果
john --show /tmp/password.db
```

### 2. 文件系统安全加固

```bash
# 锁定关键文件（immutable属性，不可修改/删除）
sudo chattr +i /etc/passwd
sudo chattr +i /etc/shadow
sudo chattr +i /etc/hosts
sudo chattr +i /etc/fstab
sudo chattr +i /etc/sudoers

# 日志文件加append-only属性（只能追加，不能删除/修改）
sudo chattr +a /var/log/messages
sudo chattr +a /var/log/secure

# 查看文件属性
lsattr /etc/passwd
```

### 3. 安全检查命令

```bash
# 查找任何用户可写的文件
find / -type f -perm -2 -o -perm -20 | xargs ls -al

# 查找任何用户可写的目录
find / -type d -perm -2 -o -perm -20 | xargs ls -ld

# 查找SUID/SGID程序（可能被用于提权）
find / -type f -perm -4000 -o -perm -2000 -print | xargs ls -al

# 查找无属主文件（孤儿文件，可能被利用）
find / -nouser -o -nogroup
```

### 4. 入侵痕迹排查

```bash
# 查看当前登录用户
who

# 锁定可疑用户
passwd -l suspicious_user

# 踢掉可疑用户
ps -ef | grep @pts/1          # 找到进程号
kill -9 <PID>                  # 强制终止

# 查看登录历史
last

# 检查木马文件
# 查找含getRuntime的JSP文件（WebShell特征）
find . -type f -name "*.jsp" | xargs grep -i "getRuntime"

# 查找含getHostAddress的文件（反弹Shell特征）
find . -type f -name "*.jsp" | xargs grep -i "getHostAddress"

# 查找JSP木马
find . -type f -name "*.jsp" | xargs grep -i "jspspy"

# 查看认证日志
cat /var/log/auth.log

# 查看登录记录
cat /var/log/wtmp

# 查找临时目录可疑文件
find / -name "*.elf" | xargs ls -l
```

### 5. 密码安全策略（PAM模块）

```bash
# 安装密码质量模块
sudo dnf install -y pam_pwquality

# 配置密码复杂度 /etc/security/pwquality.conf
minlen = 12          # 最少12位
dcredit = -1         # 至少1个数字
ucredit = -1         # 至少1个大写
lcredit = -1         # 至少1个小写
ocredit = -1         # 至少1个特殊字符

# 配置账号锁定 /etc/pam.d/system-auth
auth required pam_tally2.so deny=5 unlock_time=600
# 5次失败后锁定600秒
```

## 常见问题与排错

| 问题 | 原因 | 解决 |
|------|------|------|
| chattr +i后无法修改 | immutable属性 | `chattr -i` 解除 |
| John破解速度慢 | 字典太小 | 使用更大的字典文件 |
| 误杀正常进程 | PID判断错误 | 确认`ps -ef`输出再kill |
| SUID程序误删 | 系统依赖 | 删除前确认程序用途 |

## 速记口诀

> **John破密chattr锁，SUID提权要排查，who看登录last历史，auth.log查痕迹。**
