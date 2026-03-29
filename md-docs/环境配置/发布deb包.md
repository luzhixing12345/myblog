
# 发布deb包

1. 注册 Launchpad 账号

https://launchpad.net/

2. 创建 GPG 密钥

```bash
gpg --full-generate-key
```

# 选择 RSA (默认) 和 4096 位长度
# 设置有效期（推荐选择 0 永不过期）
# 输入你的姓名、邮箱等信息

```bash
gpg --armor --export your-email@example.com > public-key.txt
```

```bash
sudo apt install ubuntu-dev-tools
```

https://keys.openpgp.org/

```bash
gpg --fingerprint
```


```bash
/home/lzx/.gnupg/pubring.kbx
----------------------------
pub   rsa3072 2026-01-23 [SC]
      552B DAE7 659B 6471 00A1  F489 C829 9F20 164E FC27
uid           [ultimate] kamilu <luzhixing12345@163.com>
sub   rsa3072 2026-01-23 [E]
```

```bash
sudo apt install -y debhelper devscripts build-essential lintian
```

```bash
tar -tJf ../kperf_0.1.0.tar.xz
```
