---
title: mysql使用
date: 2023-07-31 13:59:41
tags: 环境配置
---

## 前言

尽管数据库, SQL 在生产中可以说是鼎鼎大名, 但很遗憾笔者只是有一些模糊的印象, 也并没有动手实践

本文简要介绍一下如何在 Debian 服务器安装 mysql, 以及 SQL 语法的简要介绍

## 安装与使用

> [digitalocean how-to-install-the-latest-mysql-on-debian-10](https://www.digitalocean.com/community/tutorials/how-to-install-the-latest-mysql-on-debian-10)
>
> [其他 mysql 安装方法](https://www.runoob.com/mysql/mysql-install.html)

### 添加 MySQL 软件存储库

```bash
sudo apt update
sudo apt install gnupg
```

打开链接 [mysql dev](https://dev.mysql.com/downloads/repo/apt/), 选择 download 并复制链接地址以安装最新版

![20230731140625](https://raw.githubusercontent.com/learner-lu/picbed/master/20230731140625.png)

![20230731140647](https://raw.githubusercontent.com/learner-lu/picbed/master/20230731140647.png)

笔者此时版本为 0.8.26

```bash
wget https://dev.mysql.com/get/mysql-apt-config_0.8.26-1_all.deb
sudo dpkg -i mysql-apt-config_0.8.26-1_all.deb
```

在安装过程中会出现配置屏幕, 使用向下箭头导航到Ok菜单选项并点击ENTER.

刷新apt软件包缓存以使新软件包可用

```bash
sudo apt update
```

现在您已经添加了 MySQL 存储库,您就可以安装实际的 MySQL 服务器软件了

### 安装 MySQL

使用apt安装最新的 MySQL 服务器包:

```bash
sudo apt install mysql-server
```

下载过程中需要输入密码, 选择 yes

使用以下方法检查systemctl, 该Active: active (running)行表示 MySQL 已安装并正在运行

```bash
sudo systemctl status mysql
```

![20230731141052](https://raw.githubusercontent.com/learner-lu/picbed/master/20230731141052.png)

### 保护 MySQL

MySQL 附带了一个命令,可以在新安装上执行一些与安全相关的更新

```bash
mysql_secure_installation
```

首先,系统会询问您有关验证密码插件的信息,该插件可以自动为您的 MySQL 用户强制执行某些密码强度规则.您需要根据自己的个人安全需求来决定启用此功能.**写入y并按ENTER以启用它**,系统会提示您选择 0-2 之间的级别来确定密码验证的严格程度.选择一个号码并按ENTER继续.

接下来,系统会询问您是否要更改root密码.由于您最近在安装 MySQL 时创建了密码,因此您可以安全地跳过此步骤.**按ENTER继续**而不更新密码.

**其余的提示可以回答yes**.系统将询问您有关删除匿名 MySQL 用户、禁止远程root登录、删除test数据库以及重新加载权限表的信息,以确保之前的更改正确生效.这些都是好主意.为每一个写下y并按下ENTER.

## MySQL 使用

登录

```bash
mysql -u root -p
```

退出输入 exit 或者使用 <kbd>ctrl</kbd> + <kbd>d</kbd> 

```bash
mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.01 sec)
```