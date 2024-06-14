---
title: VMware虚拟机配置
date: 2023-02-28 11:44:19
tags: 环境配置
---

正常来说 VMWARE 提供了虚拟机的图形界面, 笔者个人倾向于使用 Vscode, 刚好 Vscode 有比较好的远程连接的功能, 所以没有必要在 VMware 中写代码, 只需要开启 VMware 的 Linux 主机, 然后远程连接在本地(windows) 中流畅的写代码, 在本地使用ssh连接虚拟机的终端

## VMware与主机SSH

首先需要查看一下ip

```bash
sudo apt update
sudo apt install net-tools
```

```bash
kamilu@ubuntu:~$ ifconfig
```

这里显示的是 `192.168.179.139` 为我的虚拟机的ip地址, **下面的对应ip需要改为你的实际结果**

```bash
ens33     Link encap:Ethernet  HWaddr 00:0c:29:2a:5e:ef  
          inet addr:192.168.179.139  Bcast:192.168.179.255  Mask:255.255.255.0
          inet6 addr: fe80::a63f:f3c5:d9cb:1489/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:62 errors:0 dropped:0 overruns:0 frame:0
          TX packets:106 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:23047 (23.0 KB)  TX bytes:12551 (12.5 KB)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:200 errors:0 dropped:0 overruns:0 frame:0
          TX packets:200 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:16319 (16.3 KB)  TX bytes:16319 (16.3 KB)
```

安装ssh相关的 client server

```bash
sudo apt-get install openssh-client
sudo apt-get install openssh-server
sudo /etc/init.d/ssh restart
netstat -tpl
```

看到ssh成功启动即为成功

```bash
root@ubuntu:/home/kamilu# sudo /etc/init.d/ssh restart
[ ok ] Restarting ssh (via systemctl): ssh.service.
root@ubuntu:/home/kamilu# netstat -tpl
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 ubuntu:domain           *:*                     LISTEN      1016/dnsmasq    
tcp        0      0 *:ssh                   *:*                     LISTEN      3174/sshd       
tcp        0      0 localhost:ipp           *:*                     LISTEN      783/cupsd       
tcp6       0      0 [::]:ssh                [::]:*                  LISTEN      3174/sshd       
tcp6       0      0 ip6-localhost:ipp       [::]:*                  LISTEN      783/cupsd
```

最后检查一下防火墙是不是关闭了

```bash
sudo ufw status
# inactive 表示关闭
```

## 主机的操作

- vmware workstation -> 编辑 -> 虚拟网络适配器 -> 更改设置(管理员权限)

  ![20230228234333](https://raw.githubusercontent.com/learner-lu/picbed/master/20230228234333.png)

- 选择VMnet8, 点击 NAT设置

  ![20230228234503](https://raw.githubusercontent.com/learner-lu/picbed/master/20230228234503.png)

- 点击添加

  主机端口22, 虚拟机IP(刚刚ifconfig看到的192.168.179.139), 虚拟机端口22

  ![20230228234609](https://raw.githubusercontent.com/learner-lu/picbed/master/20230228234609.png)

  > 如果有很多个虚拟机都需要链接的话换一个主机端口,比如500就行了, 主机端口不能冲突

- 退出, 应用, 确定
- 主机处终端使用ssh连接

  ```bash
  ssh <NAME>@<IP>
  # ssh kamilu@192.168.179.139
  ```

  选择yes,连接成功

  ![20230228234937](https://raw.githubusercontent.com/learner-lu/picbed/master/20230228234937.png)

- host 配置

  找到 `C:\Windows\System32\drivers\etc 下的 hosts, 使用记事本打开(需要管理员权限)

  然后添加一行是你的 IP 地址, 重命名一下方便我们使用名字而不是 IP

  ```bash
  192.168.232.139 ubuntu2204
  ```

  接下来就可以使用 `ssh kamilu@ubuntu2204` 连接了

  如果 hosts 保存没有权限, 那么可以点击属性, 然后为当前用户添加完全控制

  ![20231202105657](https://raw.githubusercontent.com/learner-lu/picbed/master/20231202105657.png)

- 免密码

  关于SSH免密只需要把主机处的公钥 即找到你的 ~/.ssh/ 下的 `id_rsa.pub`, 复制到`~/.ssh/authorized_keys`文件中即可

## Vscode + SSH

Vscode的环境就是使用远程资源管理器登录,由于过程比较简单,推荐几个比较详细的配置流程,如果新手小白遇到了一些问题可以参考

- https://zhuanlan.zhihu.com/p/68577071
- https://www.cnblogs.com/huoyanCC/p/14730244.html

关于SSH免密只需要把主机处的公钥复制到`~/.ssh/authorized_keys`文件中即可

## 443端口

这个问题很恶心, 就是会出现443端口被占用导致出现一些问题

如下两个方法并没有解决我的问题

- https://blog.csdn.net/bwlab/article/details/46953569
- https://zhuanlan.zhihu.com/p/376328486

![20230306162523](https://raw.githubusercontent.com/learner-lu/picbed/master/20230306162523.png)

我的VMware是16.2, 没有 `C:\ProgramData\VMware\hostd`, 也没有共享虚拟机

一种暂时的解决措施是配置网络代理,然后配置主机的network代理http映射到20171,走代理

这个问题暂时搁置, 等以后学明白了再回来解决

## 参考

- [windows宿主机如何SSH连接VMware的Linux虚拟机](https://cloud.tencent.com/developer/article/1679861)