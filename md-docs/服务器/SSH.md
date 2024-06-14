---
title: SSH
date: 2023-02-28 11:13:39
tags: 服务器
---

> 关于git + github 的SSH连接在git ssh中记录了,这里不再赘述

## 服务器免密SSH

实际开发之中我倾向于使用Vscode远程开发,不得不说Vscode的SSH服务实在是香,很方便,Vscode界面还好看,有插件,真棒

1. 生成 rsa公钥私钥

   ```bash
   ssh-keygen -t rsa -C "luzhixing12345@163.com"
   ```
   
   **如果已经生成过一个rsa密钥了,那么换一个名字比如 id_rsa_server**


2. 在本地主机处将`id_rsa.pub`传入服务器,传入/root/目录下

   ```bash
   scp ~/.ssh/id_rsa.pub root@IP:/root
   ```

3. 登录远程主机,加入信任列表

   ```bash
   ssh root@IP
   cat /root/id_rsa.pub >> ~/.ssh/authorized_keys
   ```

4. 在进行本机ssh登录的时候就要求验证,选择yes认证之后就可以免密登录了

   ```bash
   ssh root@IP
   ```

## git SSH

> 以下案例中使用的邮箱是 `luzhixing12345@163.com` 你只需要替换为你自己的邮箱即可

- 创建SSH key

  ```shell
  ssh-keygen -t rsa -C "luzhixing12345@163.com"
  ```

- 默认路径保存,文件保存在 `c:/user/luzhi/.ssh`(Windows) 或者 `~/.ssh`(GNU/Linux)

  如果你需要创建多个SSH,比如远程连接多台服务器,Github+SSH,请手动设置不同的名字加以区分,比如 `id_rsa_server`,**SSH私钥不能共用,一对一连接**

- 不设置密码,跳过
- 然后会在上面的文件夹中生成`id_rsa`(私钥)和`id_rsa.pub`(公钥),**私钥不要泄露!**
- 打开Github->settings->SSH and GPG keys->new SSH key
- title随便起,将`id_rsa.pub`复制到下方

  ```bash
  cat ~/.ssh/id_rsa.pub
  ```

- 确定后不久会收到Github的邮件
- 在git bash中输入,注意就是`git@github.com`不是你的邮箱,该操作是将你的邮箱与github建立连接

  ```shell
  ssh -T git@github.com
  ```

  如果在这里出错显示需要输入git@github.com的密码则需要额外配置一下config文件

  在.ssh目录下新建一个config文件,目的是将SSH映射到443端口处. 配置完毕后再次重连

  ```txt
  Host github.com
    User luzhixing12345@163.com
    Hostname ssh.github.com
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/id_rsa
    Port 443
  ```

- yes
  >SSH协议采用由人工判断公钥的fingerprint是否可信的方式.当使用ssh命令连接服务器时,命令行会提示如下信息:
  >
  > The authenticity of host '168.30.9.213 (\<no hostip for proxy command\>) can't be established.
  RSA key fingerprint is 23:42:c1:e4:3f:d2:cc:37:1d:89:cb:e7:5d:be:5d:53.
  Are you sure you want to continue connecting (yes/no)?

- 如果出现Hi "用户名"! You've successfully authenticated, but GitHub does not provide shell access则设置成功
- **之后使用ssh的地址`git@github.com:xxx`而不是https的地址`https://github.com/xxx`**

## 延长SSH连接时间

```bash
vim ~/.ssh/config
```

```txt
Host *
  ServerAliveInterval 60
```

> [ServerAliveInterval含义](https://unix.stackexchange.com/questions/3026/what-do-options-serveraliveinterval-and-clientaliveinterval-in-sshd-config-d)

## 域名替换

```bash
sudo vim /etc/hosts
# Windows
C:\Windows\System32\drivers\etc\hosts
```

补充一条 `IP 域名` 即可