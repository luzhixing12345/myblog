---
title: WSL2配置
date: 2022-10-06 17:35:04
tags: 环境配置
---

## WSL

> [官方文档](https://learn.microsoft.com/zh-cn/windows/wsl/install)

### 安装 WSL

Windows可以使用WSL(**W**indows **S**ubsystem for **L**inux)来使用Linux环境

1. 打开控制面板->程序

   ![20220924231310](https://raw.githubusercontent.com/learner-lu/picbed/master/20220924231310.png)

2. 启动或关闭 Windows 功能

   ![20220924233547](https://raw.githubusercontent.com/learner-lu/picbed/master/20220924233547.png)

3. 开启 "适用于 Linux 的 Windows 子系统" 和 "虚拟机平台" 选项

   ![20220924233650](https://raw.githubusercontent.com/learner-lu/picbed/master/20220924233650.png)

   启用服务,重启电脑

4. 键盘按下 <kbd>Win</kbd> + <kbd>r</kbd> 输入 cmd 后回车

   ```bash
   wsl --install -d Ubuntu
   ```

   当然我们也可以选择其他操作系统,可以通过如下命令查看可用发行版列表

   ```bash
   wsl --list --online
   ```

   ![20221020002852](https://raw.githubusercontent.com/learner-lu/picbed/master/20221020002852.png)

5. 等待安装完毕之后,输入用户名 密码就可以进入Linux系统了,这个操作系统的名字是 Ubuntu

   如果**关闭窗口后再想重新进入这个系统**,只需要在命令行中输入 wsl 或者这个操作系统的名字就可以直接进入

   当然也支持[安装运行多个操作系统](https://learn.microsoft.com/zh-cn/windows/wsl/install#ways-to-run-multiple-linux-distributions-with-wsl),不过暂时没有这个必要

### WSL 中使用gdb调试

1. 检查系统中是否已经安装了gdb

   ```bash
   gdb -v
   ```

2. 如果没有安装,则使用命令行安装

   ```bash
   sudo apt-get update
   sudo apt-get install build-essential gdb
   ```

   <details><summary>如果下载太慢了</summary>

   考虑切换一个下载的源

   ```bash
   vim /etc/apt/sources.list
   ```

   在文件最前面加入 / 删除整个文件重新创建一个新的文件并写入

   ```txt
   deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
   deb-src http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
   deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
   deb-src http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
   deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
   deb-src http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
   deb http://mirrors.aliyun.com/ubuntu/ jammy-proposed main restricted universe multiverse
   deb-src http://mirrors.aliyun.com/ubuntu/ jammy-proposed main restricted universe multiverse
   deb http://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse
   deb-src http://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse
   ```

   保存退出,重新执行

   > [其他源](https://blog.csdn.net/xiangxianghehe/article/details/122856771)

   </details>

3. 查看WSL版本

   ```bash
   wsl --list --verbose
   ```

   如果是WSL1的运行gdb会出现问题,升级到WSL2

   > [Github Issue1](https://github.com/microsoft/WSL/issues/8356)
   >
   > [Github Issue2](https://github.com/microsoft/WSL/issues/8516)

   **回到Windows系统的命令行**, 升级WSL系统

   ```bash
   wsl --set-version Ubuntu 2
   ```

### WSL 与 Windows文件互传

WSL正常情况下会出现在文件资源管理器,可以直接在 home 目录下找到当前安装的操作系统

![20221020002321](https://raw.githubusercontent.com/learner-lu/picbed/master/20221020002321.png)

如果安装之后没有找到, 可以通过其他方式

- <kbd>win</kbd> + <kbd>r</kbd> 输入 `\\wsl$`
- 进入wsl的操作系统中,在终端中输入 `explorer.exe .`

我们可以直接打开两个文件夹,直接通过复制粘贴实现文件传输

除此之蛙wsl将windows中的文件挂载到 /mnt 虚拟磁盘下,默认的登录路径也是这里,我们可以直接通过mnt切换盘符及路径,比如:

```bash
kamilu@LZX:/mnt/c/Users/luzhi$ cd /mnt/d
kamilu@LZX:/mnt/d$
```

再利用 cp 或者 mv 命令就可以实现文件的传输了,笔者这里还是推荐第一种,比较直接

### 安装一个更加美观的 Terminal 终端

原生的命令行窗口并不好看,由于本实验可能需要大部分时间面对一个终端的显示,我们考虑选择使用一个更加美观漂亮的终端

在 [terminal release](https://github.com/microsoft/terminal/releases) 中下载最新版的安装包

注意区分 Win10/11版本,不要下错了

> 如果不清楚windows版本可以按下<kbd>Win</kbd> + <kbd>r</kbd> 输入 winver查看

![20220925010349](https://raw.githubusercontent.com/learner-lu/picbed/master/20220925010349.png)

下载后点击对应版本安装即可,接下来尝试再来按下 <kbd>Win</kbd> + <kbd>r</kbd> 输入cmd进入控制台吧,是不是好看多了?

## WSL2代理配置

WSL2由于直接使用局域网与本机通信,可以直接使用Windows上的代理端口,这里假定读者已安装过 Windows 下的 [V2ray](https://me.tofly.cyou/)

---

## 修改V2ray默认选项

设置->参数设置->允许来自局域网的连接

![20221023180045](https://raw.githubusercontent.com/learner-lu/picbed/master/20221023180045.png)

### 查看代理端口

![20221023180208](https://raw.githubusercontent.com/learner-lu/picbed/master/20221023180208.png)

http的系统代理走局域网的10811端口

### 修改.bashrc文件

打开.bashrc

```bash
vim ~/.bashrc
```

在文件结尾加入

```bash
export host_ip=$(cat /etc/resolv.conf |grep "nameserver" |cut -f 2 -d " ")
export http_proxy="http://$host_ip:10811"
export https_proxy="http://$host_ip:10811"
```

:wq保存退出,激活环境

```bash
source ~/.bashrc
```

### 测试

```bash
wget www.google.com
wget https://raw.githubusercontent.com/luzhixing12345/MyScripts/main/main.py
```

得到两个文件即为成功

### 直连域名配置

正常使用v2ray会出现访问一些服务器的域名无法访问,但是直连可以访问.这时候需要 设置-路由设置-直连的Domain/IP

## SSH 失败

之前有一段时间突然发现 git 一直push不上去, 也pull不下来

然后使用 `ssh -vT git@github.com` 查看发现原来是 SSH 的问题, 一直卡在下面的这个地方

```bash
debug1: expecting SSH2_MSG_KEX_ECDH_REPLY
```

后来查阅了一些资料, 在 [Github cloning error in wsl2 (driver MTU)](https://github.com/microsoft/WSL/issues/4253) 得到了解决

总结一下就是先[下载网卡驱动](https://www.intel.com/content/www/us/en/download/19351/windows-10-and-windows-11-wi-fi-drivers-for-intel-wireless-adapters.html?product=99446)

正常来说你安装完网卡驱动应该就可以解决了, 重启一下, 要不就等一下

如果仍然有问题: 用 `ip addr | grep mtu` 看下 eth0 的 mtu

```bash
(base) kamilu@LZX:~$ ip addr | grep mtu
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
2: bond0: <BROADCAST,MULTICAST,MASTER> mtu 1500 qdisc noop state DOWN group default qlen 1000
3: dummy0: <BROADCAST,NOARP> mtu 1500 qdisc noop state DOWN group default qlen 1000
4: tunl0@NONE: <NOARP> mtu 1480 qdisc noop state DOWN group default qlen 1000
5: sit0@NONE: <NOARP> mtu 1480 qdisc noop state DOWN group default qlen 1000
6: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
```

改成

```bash
sudo ifconfig eth0 mtu 1350
```

或者

```bash
sudo ip link set eth0 mtu 1400
```

## NPM 失败

安装 npm 后使用提示: /usr/bin/env: 'bash\r': No such file or directory

相关问题及解决办法见: [After installing npm on WSL](https://stackoverflow.com/questions/67938486/after-installing-npm-on-wsl-ubuntu-20-04-i-get-the-message-usr-bin-env-bash)

```bash
sudo apt install nodejs npm
```

修改 /etc/wsl.conf

```bash
sudo vim /etc/wsl.conf
```

复制下面的内容

```txt
[interop]
appendWindowsPath = false
```

重启

```bash
wsl --shutdown
wsl
```

## GUI 界面

WSL2 中执行

```bash
sudo apt install xfce4
```

Windows 中执行, 找到下面 WSL 对应的 IP 地址

```bash
ipconfig
```

![20230806120832](https://raw.githubusercontent.com/learner-lu/picbed/master/20230806120832.png)

在 ~/.bashrc 中添加, 将 IP 地址替换为你的

```bash
export DISPLAY=172.19.64.1:0
```

下载 [sourceforge vcxsrv](https://sourceforge.net/projects/vcxsrv/), 完成后点击 `xlaunch.exe` 启动, 选择 one large window, 第二个不动, 最后参数添加 `-ac`

![20230806121155](https://raw.githubusercontent.com/learner-lu/picbed/master/20230806121155.png)

启动图形化界面, 然后在 WSL2 中运行 xfce4

```bash
sudo startxfce4
```

![20230806120957](https://raw.githubusercontent.com/learner-lu/picbed/master/20230806120957.png)

![20230806121624](https://raw.githubusercontent.com/learner-lu/picbed/master/20230806121624.png)

- [通过 VcXsrv 在 WSL2 上使用图形化界面(xfce4)](https://www.cnblogs.com/blauendonau/p/14166062.html)
- [【WSL2】在你的win10/11电脑上安装Linux子系统+Ubuntu+图形化界面](https://www.bilibili.com/video/BV1mX4y177dJ/)

## 修改默认登录用户

[WSL 修改默认用户](https://blog.csdn.net/qq_37085158/article/details/131041223)

## WSL2 切换根目录位置

默认安装路径在 C 盘, 但是用久了会变大, 可以考虑移动目录到其他位置

查看虚拟机

```bash
wsl -l -v
```

> 假设名字为 Ubuntu

```bash
wsl --shutdown
```

导出 Ubuntu 保存为一个镜像, 这一步会比较慢, 相当于打一个快照以便后期恢复

```bash
wsl --export Ubuntu H:\wsl2-backup\WSL2Ubuntu.bak
```

注销原先用户

```bash
wsl --unregister Ubuntu
```

导入到一个新位置(F)

```bash
wsl --import Ubuntu F:\wsl2\ H:\wsl2-backup\WSL2Ubuntu.bak --version 2
```

导入成功后可以再次查看一下

```bash
wsl -l -v
```

如果不在第一个默认启动位置可以修改默认启动为 Ubuntu

```bash
wsl --set-default Ubuntu
```

默认使用 `wsl` 登录会以 root 用户登录, 修改为之前的用户名

```bash
Ubuntu config --default-user kamilu
```

## 参考

- [WSL修改默认安装目录到其他盘](https://www.cnblogs.com/tl542475736/p/14855863.html)
- [microsoft learn](https://learn.microsoft.com/zh-cn/windows/wsl/basic-commands)