
# Linux 代理配置

Linux 的代理配置有两种情况，第一种是局域网，第二种是互联网通用型

## 局域网

如果你的主机已经挂了代理，比如安装了 v2rayn/clash，并且是通过网线（局域网）连接的 linux 服务器，这种情况常见于学生机房。那么当你 ssh 到这台服务器可以非常简单的让它使用你主机的代理

首先你需要获取你的主机所在的局域网的 ip 地址，假设你的主机和服务器位于同一个局域网，你的ip是`192.168.1.59`，服务器ip是`192.168.1.122`

> 你的主机 ip 可以通过 ipconfig 查看

那么只需要在服务器的 bashrc 中添加如下命令即可，其中 7890 为你本机代理的端口

```bash
export http_proxy=192.168.1.59:7890
export https_proxy=192.168.1.59:7890
```

> 这个方式同 [wsl2配置](./WSL2配置.md) 的网络代理配置

## ssh 端口转发

上面这种方式更多见于局域网使用，但如果是使用 ssh 远程登录一台服务器，那么本机没有暴露 ip 可以使用就没有办法用上面的方式

此时可以采用端口转发的方式，因为主机的代理开在 7890 端口，那么我们可以在 ssh 连接的时候把 7890 端口转发，此时远程服务器上访问 7890 相当于通过 ssh 访问我们主机的 7890 端口

```bash
ssh -D 7890 lcxl2
```

然后在 .bashrc 中添加。注意此时的 ip 使用 127.0.0.1，因为端口转发过去之后服务器应当访问它自己的本地 7890 端口才能达到使用代理的效果

```bash
export http_proxy=127.0.0.1:7890
export https_proxy=127.0.0.1:7890
```

如果不想每次都使用 -D 可以写在 .ssh/config 中

```txt{4}
Host lcxl2
    User lzx
    HostName xxx
    DynamicForward 7890
```

## apt 走代理

apt 默认不会走代理，可以修改其配置文件

```bash
sudo vim /etc/apt/apt.conf.d/proxy.conf
```

```bash
Acquire::http::Proxy "http://127.0.0.1:10808";
Acquire::https::Proxy "http://127.0.0.1:10808";
```

或者如果只需要单次使用 

```bash
sudo apt -o Acquire::http::Proxy="http://127.0.0.1:10808" update
```

## V2rayA

另外的两种方式是直接在远程服务器上安装代理软件

参考官方文档 [v2rayA](https://v2raya.org/docs/prologue/introduction/),已经比较详细了,笔者个人使用的是 Debian,ubuntu同理, 这里以它为例

1. 下载并使用v2rayA 提供的镜像脚本

   ```bash
   sudo apt install curl wget
   curl -Ls https://mirrors.v2raya.org/go.sh | sudo bash
   ```

   关闭服务

   ```bash
   sudo systemctl disable v2ray --now
   ```

2. 添加公钥

   ```bash
   wget -qO - https://apt.v2raya.org/key/public-key.asc | sudo tee /etc/apt/trusted.gpg.d/v2raya.asc
   ```

3. 添加 V2RayA 软件源
  
   ```bash
   echo "deb https://apt.v2raya.org/ v2raya main" | sudo tee /etc/apt/sources.list.d/v2raya.list
   sudo apt update
   ```

   如果这一步update出错, 那就直接前往[V2rayA](https://github.com/v2rayA/v2rayA/releases)下载包手动安装

   ```bash
   wget <package.deb>
   sudo dpkg -i <package.deb>
   # 如果出现问题
   # sudo apt-get install -f
   ```

4. 安装 V2RayA

   ```bash
   sudo apt install v2raya
   ```

5. 启动并设置开机自启

   ```bash
   sudo systemctl start v2raya.service
   sudo systemctl enable v2raya.service
   ```

安装之后就可以访问到UI界面了 http://localhost:2017

> 如果是服务器配置的话还需要打开这个端口,入方向规则和出方向规则

创建账号,导入节点,这里直接使用[V2free](https://me.tofly.cyou/user)的用户的订阅链接即可

导入成功后SERVER中全选,测试HTTP连接,选择几个延迟较低的,应用即可

默认端口为20170(socks5), 20171(http), 20172(带分流规则的http) 端口

- 如果是桌面端的Ubuntu系统需要手动开启网络代理应用于本机(127.0.0.1)

  |127.0.0.1|20171|
  |:--:|:--:|
  |127.0.0.1|20171|
  |空|空|
  |127.0.0.1|20170|

  ![Screenshot from 2023-01-01 22-08-42](https://raw.githubusercontent.com/learner-lu/picbed/master/Screenshot%20from%202023-01-01%2022-08-42.png)

- 如果是服务器端可以在 `.bashrc` 最后加入配置代理端口(不要忘记如果云服务器没开放这个端口要去云服务器网站手动开启这个端口的入出方向规则)

  ```bash
  vim ~/.bashrc
  ```

  加入

  ```txt
  export http_proxy="http://localhost:20171"
  export https_proxy="http://localhost:20171"
  ```

  激活环境

  ```bash
  source ~/.bashrc
  ```

## clash for linux

> https://me.tofly.cyou/doc/#/linux/clash

进入clash的[release](https://github.com/Dreamacro/clash/releases),根据系统选择对应的文件

通常来说是linux-amd64,两个安装包都可以,选择第一个即可

```bash
wget https://github.com/Dreamacro/clash/releases/download/v1.12.0/clash-linux-amd64-v1.12.0.gz
```

> 386是对于32位的,amd64是x86

下载完成之后解压得到可执行文件

```bash
gzip -f clash-linux-amd64-v1.12.0.gz -d
```

授权可执行权限

```bash
chmod +x clash-linux-amd64-v1.12.0
```

初始化执行

```bash
./clash-linux-amd64-v1.12.0
```

初始化执行 clash 会默认在 ~/.config/clash/ 目录下生成配置文件和全球IP地址库:config.yaml 和 Country.mmdb

如果初始化出现问题可以到原网站手动下载

用wget下载clash配置文件,替换默认的配置文件,下面的wget命令后面的 你的Clash订阅链接网址 ,用上面的实际的clash订阅链接替换

这里的clash订阅地址需要到 <https://me.tofly.cyou/doc/#/linux/clash> 查看自己的

```bash
wget -U "Mozilla/6.0" -O ~/.config/clash/config.yaml  你的Clash订阅链接网址
```

再次启动clash, 这里使用后台启动, 前台启动的话如果关闭当前终端则clash代理就终止了

```bash
nohup ./clash-linux-amd64-v1.12.0 &
```

clash 默认 http 端口默认监听 7890 , socks5 端口默认监听 7891

- 如果是ubuntu桌面端手动配置代理端口即可

  ![20221115170933](https://raw.githubusercontent.com/learner-lu/picbed/master/20221115170933.png)

- 如果是服务器端可以在 `.bashrc` 最后加入配置代理端口(不要忘记如果云服务器没开放这个端口要去云服务器网站手动开启这个端口的入出方向规则)

  ```bash
  vim ~/.bashrc
  ```

  加入

  ```txt
  export http_proxy="http://localhost:7890"
  export https_proxy="http://localhost:7890"
  ```

  激活环境

  ```bash
  source ~/.bashrc
  ```
