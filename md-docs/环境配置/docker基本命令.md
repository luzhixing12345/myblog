---
title: docker基本命令
date: 2022-11-08 01:06:27
tags: 环境配置
---

# Docker

> [docker教程](https://www.runoob.com/docker/debian-docker-install.html)

## 基本架构

![20221108011126](https://raw.githubusercontent.com/learner-lu/picbed/master/20221108011126.png)

docker有两个概念,镜像和容器. 镜像相当于类,容器相当于类创建的对象. 一个镜像可以创建多个容器

## 安装docker

```bash
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```

WSL2 中安装参考 [WSL 2 上的 Docker 远程容器入门](https://learn.microsoft.com/zh-cn/windows/wsl/tutorials/wsl-containers)

> [换源](https://yeasy.gitbook.io/docker_practice/install/mirror)

安装之后可以测试运行一下 `docker ps -a`, 如果报错出现 "permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get "http://%2Fvar%2Frun%2Fdocker.sock/v1.24/containers/json?all=1": dial unix /var/run/docker.sock: connect: permission denied"

```bash
sudo usermod -aG docker $USER
newgrp docker
sudo systemctl status docker
```

即可解决

## 拉取一个Ubuntu的镜像(默认最新)

```bash
docker pull ubuntu
```

拉取特定版本的

```bash
docker pull ubuntu:16.04
```

## 查看所有镜像

```bash
docker images
```

以下内容以笔者本机为例, 笔者拉取了两个版本的Ubuntu镜像和一个默认拉取的hello-world镜像

```bash
(base) root@hecs-67846:~# docker images
REPOSITORY    TAG       IMAGE ID       CREATED         SIZE
ubuntu        latest    a8780b506fa4   4 days ago      77.8MB
hello-world   latest    feb5d9fea6a5   13 months ago   13.3kB
ubuntu        16.04     b6f507652425   14 months ago   135MB
```

## 查看容器情况

```bash
docker ps -a
```

笔者这里有一个正在运行的容器

```bash
CONTAINER ID   IMAGE          COMMAND       CREATED       STATUS       PORTS     NAMES
da1811a84ddc   ubuntu:16.04   "/bin/bash"   7 hours ago   Up 4 hours             csapp
```

## 启动一个容器

```bash
docker run --name kamilu -itd ubuntu /bin/bash
```

其中 `-it` 的 `-t` 选项让Docker分配一个伪终端(pseudo-tty)并绑定到容器的标准输入上, `-i` 则让容器的标准输入保持打开

`-d` 是笔者个人喜欢使用的,它会使容器在后台运行并且返回生成的容器的ID

后面的ubuntu指的就是镜像的名字,这里使用的ubuntu,也就是ubuntu:latest, 最后启动一个 bash 终端,允许用户进行交互

前面的 `--name` 是为这个容器指定一个名字,如果不指定的话这个名字比较随意,不是很方便管理

再使用 `docker ps -a` 查看可以看到容器已经运行起来了

```bash
CONTAINER ID   IMAGE          COMMAND       CREATED         STATUS         PORTS     NAMES
9041786640c9   ubuntu         "/bin/bash"   8 seconds ago   Up 6 seconds             kamilu
da1811a84ddc   ubuntu:16.04   "/bin/bash"   7 hours ago     Up 5 hours               csapp
```

重启一个已关闭的容器使用

```bash
docker restart <CONTAINER_ID>
```

### 容器内权限的问题

如果在服务器上运行一个 container, 如果以上述方式启动那么当内部运行的程序需要更高权限的时候会报错

1. 如果在gdb调试的时候遇到了`warning: Error disabling address space randomization: Operation not permitted`的报错,需要在 OPTION 中加入如下参数,后面一样不变

   ```bash
   docker run --cap-add=SYS_PTRACE --security-opt seccomp=unconfined
   ```

2. 如果报错类似 `Operation not permitted`, 可以在启动时加上 `--privileged` 参数

   ```bash
   docker run --privileged ...
   ```

## 进入容器

进入容器之前容器需要处于正在运行的状态,进入有两种方式 `attach` 和 `exec`

- attach 从容器退出会导致容器的停止

  ```bash
  # 直接使用容器的名字
  docker attach kamilu
  # 使用容器的ID
  docker attach 9041786640c9
  ```

- exec 退出不会导致容器停止,比较适合需要持续运行的后台服务

  ```bash
  docker exec -it kamilu /bin/bash
  ```

  > 如果需要在一个容器中使用多个终端处理不同的任务,应该使用exec的方式进入,attach会导致两个终端的状态同步

## 文件传输

主机->容器

```bash
docker cp <PATH> <CONTAINER_ID/NAME>:<PATH>
# docker cp bomb.tar csapp:/root
```

容器->主机

```bash
docker cp <CONTAINER_ID/NAME>:<PATH> <PATH>
# docker cp csapp:/home/bomb.tar /home/files
```

## 退出 关闭 删除容器

### 退出

- exit
- <kbd>ctrl</kbd> + <kbd>d</kbd>

### 关闭

```bash
docker stop <NAME>
docker stop <CONTAINER_ID>
```

## 删除容器

```bash
docker rm -f <NAME>
docker rm -f <CONTAINER_ID>
```

## 导入和导出容器

导出

```bash
docker export csapp > csapp.tar
```

导入: 从容器快照文件中再导入为镜像

```bash
docker import csapp.tar another_csapp:v1.0
```

```bash
cat csapp.tar | docker import - another_csapp:v1.0
```

## 删除镜像

```bash
docker rmi another_csapp:v1.0
```

## 上传容器

首先需要前往[docker hub](https://hub.docker.com/)注册一个账号,假设账号名为kamidalu

你希望上传的容器名为miniCRT,你需要先将其打包成 Docker 镜像,注意打包的名字里面不能有大写字符

```bash
docker commit miniCRT kamidalu/minicrt
```

登录docker账号

```bash
docker login
```

如下结果为登录成功

```bash
Authenticating with existing credentials...
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
```

上传你的docker镜像

```bash
docker push kamidalu/minicrt
```

## 基础环境搭建

纯docker容器相当的干净,可以快速地把常用软件安装一下,以便后续使用

- 基本

```bash
apt-get -y update
apt-get -y install sudo
sudo apt -y install vim
sudo apt -y install wget
sudo apt -y install unzip
```

- 软件

```bash
sudo apt -y install git
```

- C

```bash
sudo apt -y install gcc
sudo apt -y install build-essential gdb
sudo apt -y install gcc-multilib
```

## Docker 代理配置

docker代理配置的也很简单,并且官方提供了镜像,我们只需要直接运行就可以拉取镜像创建容器了

如果你的本机已经配置了代理,那么只需要在创建的时候加入`--network=host` 即可(不过似乎有点小问题...)

```bash
docker run -itd --network=host --name=<NAME> ubuntu
```

```bash
docker run -d \
  --restart=always \
  --privileged \
  --network=host \
  --name v2raya \
  -e V2RAYA_ADDRESS=0.0.0.0:2017 \
  -v /lib/modules:/lib/modules:ro \
  -v /etc/resolv.conf:/etc/resolv.conf \
  -v /etc/v2raya:/etc/v2raya \
  mzz2017/v2raya
```

值得注意的是镜像制作使用的是 alpine linux ,所以进入的话需要使用 `/bin/sh`

```bash
docker exec -it v2raya /bin/sh
```

并且默认源太慢了,可以换成中科大的源(推荐)

```bash
sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
```

或者阿里的镜像源

```bash
sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
```

> alpine linux下载使用的是 `apk add <name>` 而不是 `apt install <name>`

```bash
apt-get install apt-transport-https ca-certificates
```
