
# cube

日志

```bash
/var/log/cube-sandbox-one-click
```

Go 安装依赖

```bash
GOPROXY=https://goproxy.cn,direct go mod install
```

```bash
CUBE_PROXY_HTTP_HOST_PORT
```

```bash
sudo ip tuntap show \
    | awk '/^z192[.]168[.]/ {sub(":", "", $1); print $1}' \
    | while read -r dev; do
        sudo ip tuntap del dev "$dev" mode tap
      done
sudo ip link delete cube-dev
```

```bash
# 1. 安装 XFS 工具（如果还没有）
sudo apt-get update && sudo apt-get install -y xfsprogs   # Debian/Ubuntu
# 或
sudo yum install -y xfsprogs                               # CentOS/RHEL

# 2. 创建 2GB 的空磁盘文件（放在 /data 下即可）
sudo fallocate -l 2G /data/cubelet.img
# 如果 fallocate 不支持，用 dd：
# sudo dd if=/dev/zero of=/data/cubelet.img bs=1M count=2048

# 3. 格式化为 XFS
sudo mkfs.xfs /data/cubelet.img

# 4. 创建挂载点并挂载
sudo mkdir -p /data/cubelet
sudo mount /data/cubelet.img /data/cubelet

# 5. 验证
df -Th /data/cubelet
mount | grep cubelet
```

xfs img 空间不足扩容

```bash
df -h /data/cubelet
df -ih /data/cubelet
findmnt -T /data/cubelet

sudo truncate -s 50G /data/cubelet.img
sudo losetup -c /dev/loop1
```

设置开机自挂载，编辑 `/etc/fstab`

```bash
/data/cubelet.img /data/cubelet xfs loop,defaults 0 0
```

sudo nsenter -t "$(pgrep -f '/Cubelet/bin/cubelet' | head -n1)" -m -- findmnt -n -o TARGET,SOURCE,FSTYPE,OPTIONS 

/data/cubelet/hostdir/

│ ├─/data/cubelet/hostdir/9847ba94c3b345c99222b30bf1ae0e9d/rw/hostdir-0
│ │     /dev/sda2[/tmp/rw]
│ │            ext4        rw,relatime,errors=remount-ro,stripe=16
│ └─/data/cubelet/hostdir/9847ba94c3b345c99222b30bf1ae0e9d/ro/hostdir-1
│       /dev/sda2[/tmp/ro]
│              ext4        ro,relatime,errors=remount-ro,stripe=16