---
title: Ubuntu工作环境配置
date: 2022-11-15 15:59:08
tags: 环境配置
---

## 前言

如今Linux发行版不少,也有各种好看的Linux桌面.如果只是想使用一个Linux的环境+bash那么无论是WSL还是SSH到一台远程服务器都是比较方便的,或者docker创建一个Linux的环境等等,配合Vscode做各种代码开发我想应该都是老生常谈的事情了.

本文用于记录笔者在Ubuntu22.04桌面版的工作环境配置,包括各种笔者认为**必要的软件的安装,配置修改和个人偏好**,主要目的有两个

另外笔者使用的是Ubuntu22.04的操作系统,对于老版本和更新的版本有一些出入,还请各位注意

## 换源

```bash
sudo apt install vim git
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo vim /etc/apt/sources.list
```

删除所有内容,然后在最开头添加中科大源

```txt
deb https://mirrors.ustc.edu.cn/ubuntu/ jammy main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ jammy main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ jammy-security main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ jammy-security main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ jammy-proposed main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ jammy-proposed main restricted universe multiverse
```

- [22.04源](https://blog.csdn.net/xiangxianghehe/article/details/122856771)
- [20.04源](https://zhuanlan.zhihu.com/p/142014944)
- [18.04源](https://zhuanlan.zhihu.com/p/61228593)
- [16.04源](https://www.jianshu.com/p/b2288ef3f11e)

```bash
sudo apt update
```

有时候 apt install 会有 lock 的问题: apt-get /var/lib/dpkg/lock-frontend

```bash
sudo rm /var/lib/dpkg/lock-frontend
sudo rm /var/lib/dpkg/lock
sudo rm /var/cache/apt/archives/lock
```

## 创建用户

```bash
sudo useradd lzx
```

为新用户添加 sudo 权限

```bash
sudo vim /etc/sudoers
```

在 root 下面加一行

```txt
root    ALL=(ALL:ALL) ALL
lzx     ALL=(ALL:ALL) ALL
```

## Ubuntu基础配置

- 在跳出自动更新的时候,顺势进入setting将自动更新时间修改为Never
- privacy->息屏时间调为永不

  ![Screenshot from 2023-01-01 22-49-50](https://raw.githubusercontent.com/learner-lu/picbed/master/Screenshot%20from%202023-01-01%2022-49-50.png)

- Software下载screenshot

  设置中将截图快捷键修改为 ctrl + alt + a(QQ的默认截图快捷键),默认的截图保存在 `~/Picture/Screenshot`,笔者一般配合vscode+picgo传到GitHub图床

  ![Screenshot from 2023-01-01 22-08-22](https://raw.githubusercontent.com/learner-lu/picbed/master/Screenshot%20from%202023-01-01%2022-08-22.png)

  ![Screenshot from 2023-01-01 22-07-08](https://raw.githubusercontent.com/learner-lu/picbed/master/Screenshot%20from%202023-01-01%2022-07-08.png)

- terminal配置

  在上方keyboard相同位置,搜索terminal,修改唤起快捷键为 option + r (同windows下win+r)

  ![Screenshot from 2023-01-01 22-53-31](https://raw.githubusercontent.com/learner-lu/picbed/master/Screenshot%20from%202023-01-01%2022-53-31.png)

  唤起terminal,perference,uname

  背景颜色改为黑色,字体色白色,略微放大字体,修改字体为ubuntu bone

- 下载vscode
  
  进入[官网](https://code.visualstudio.com/download),对于ubuntu下载deb即可

  不要使用ubuntu的software来安装vscode,存在中文无法输入的问题,到官网下载linux版本的

  同步一下扩展

  安装picgo依赖

  ```bash
  sudo apt install xclip
  ```

  ![20230103111043](https://raw.githubusercontent.com/learner-lu/picbed/master/20230103111043.png)

- 精简左侧默认任务栏

## 网络代理

因为众所周知的原因,我们需要配置一下网络代理,解决代理问题之后我们就可以推进很多工作了

笔者个人倾向于v2rayA,比较省事.参考官方文档 [v2rayA](https://v2raya.org/docs/prologue/introduction/)

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

![20230222182331](https://raw.githubusercontent.com/learner-lu/picbed/master/20230222182331.png)

默认端口为20170(socks5), 20171(http), 20172(带分流规则的http) 端口

桌面端的Ubuntu系统需要手动开启网络代理应用于本机(127.0.0.1)

| 127.0.0.1 | 20171 |
| :-------: | :---: |
| 127.0.0.1 | 20171 |
|    空     |  空   |
| 127.0.0.1 | 20170 |

![Screenshot from 2023-01-01 22-08-42](https://raw.githubusercontent.com/learner-lu/picbed/master/Screenshot%20from%202023-01-01%2022-08-42.png)

## 安装中文输入法

- setting->region and language->manage installed language(打开之后会让你安装)
- 安装ficitx5

  ```bash
  sudo apt install fcitx5 \
  fcitx5-chinese-addons \
  fcitx5-frontend-gtk3 fcitx5-frontend-gtk2 \
  fcitx5-frontend-qt5 kde-config-fcitx5
  ```
  
  > 如果不是ubuntu22.04版本的话最后一项会报错找不到, 其他版本的中文输入法安装见: <https://zhuanlan.zhihu.com/p/529892064>

- 中文词库

  在 GitHub 打开[维基百科中文拼音词库](https://link.zhihu.com/?target=https%3A//github.com/felixonmars/fcitx5-pinyin-zhwiki)的 [Releases](https://link.zhihu.com/?target=https%3A//github.com/felixonmars/fcitx5-pinyin-zhwiki/releases) 界面,下载最新版的 .dict 文件

  先运行一下fcitx5创建一下.local/share目录

  ```bash
  fcitx5
  ```

  然后ctrl+c退出即可

  ```bash
  wget https://github.com/felixonmars/fcitx5-pinyin-zhwiki/releases/download/0.2.4/zhwiki-20220416.dict
  mkdir ~/.local/share/fcitx5/pinyin/
  mkdir ~/.local/share/fcitx5/pinyin/dictionaries/
  mv zhwiki-20220416.dict ~/.local/share/fcitx5/pinyin/dictionaries/
  ```

- 设置为fcitx5默认输入法

  setting->region and language->manage installed language, 切换ibus为fcitx5

- 环境变量

  ```bash
  vim ~/.bashrc
  ```

  shift+G切到最下面,添加

  ```txt
  export XMODIFIERS=@im=fcitx
  export GTK_IM_MODULE=fcitx
  export QT_IM_MODULE=fcitx
  ```

  保存退出,激活

  ```bash
  source ~/.bashrc
  ```

- 开机自启动

  ```bash
  sudo apt install gnome-tweaks
  gnome-tweaks
  ```

  ![Screenshot from 2023-01-01 22-35-04](https://raw.githubusercontent.com/learner-lu/picbed/master/Screenshot%20from%202023-01-01%2022-35-04.png)

- 修改默认fcitx5配置

  ```bash
  fcitx5-configtool
  ```

  打开GUI后取消勾选 only show current language,将pinyin移至左侧,apply

  > 这里english在第一个,pinyin第二个

  ![Screenshot from 2023-01-01 22-37-00](https://raw.githubusercontent.com/learner-lu/picbed/master/Screenshot%20from%202023-01-01%2022-37-00.png)

- 切简体中文

  ctrl+space切换输入法为pinyin(可以在addons中修改,这里保持默认不修改),点击traditional chinese切换为simplified chinese

  ![Screenshot from 2023-01-01 23-43-55](https://raw.githubusercontent.com/learner-lu/picbed/master/Screenshot%20from%202023-01-01%2023-43-55.png)

  然后你就可以打字了

- 输入法美化

  这个因人而异,可以[搜索fcitx5](https://github.com/search?q=fcitx5+theme&type=Repositories)其他主题

  笔者这里使用的是[nord](https://github.com/tonyfettes/fcitx5-nord)主题,[alpha-black](https://github.com/sxqsfun/fcitx5-sogou-themes)这款我也比较喜欢

  ```bash
  git clone https://github.com/tonyfettes/fcitx5-nord.git
  mkdir -p ~/.local/share/fcitx5/themes/
  cd fcitx5-nord
  cp -r Nord-Dark/ Nord-Light/ ~/.local/share/fcitx5/themes/
  ```

  切换classic user interface

  ![Screenshot from 2023-01-01 23-39-39](https://raw.githubusercontent.com/learner-lu/picbed/master/Screenshot%20from%202023-01-01%2023-39-39.png)

  最后效果大概这样

  ![Screenshot from 2023-01-01 23-40-06](https://raw.githubusercontent.com/learner-lu/picbed/master/Screenshot%20from%202023-01-01%2023-40-06.png)

## Chrome

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
```

接着就可以找到chrome了,这里有可能出现chrome图标找不到的问题,打开chrome也可能卡死,不过重启一下或者重新dpkg装一下似乎就好了,~~然后就可以把firefox卸了~~

ubuntu的话默认fn键是启用的,所以F12这里会调整音量,永久禁用(重启生效)

```bash
echo options hid_apple fnmode=0 | sudo tee -a /etc/modprobe.d/hid_apple.conf
sudo update-initramfs -u -k all
```

> 暂时性的禁用和启用fn见 https://www.bilibili.com/read/cv14517991/

然后同步一下google账号

## Vim

这里直接用了我的个人vimrc配置,大家可以换成自己的,我改的不是很多

```bash
curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
wget https://raw.githubusercontent.com/luzhixing12345/vimrc/main/.vimrc
vim .vimrc
:PlugInstall
```

## 软件安装

deepin-wine

```bash
sudo apt-get update
wget -O- https://deepin-wine.i-m.dev/setup.sh | sh
```

![20230228113320](https://raw.githubusercontent.com/learner-lu/picbed/master/20230228113320.png)

看到如下界面说明成功了,然后 **关闭当前终端新开一个终端**

```bash
# 微信
sudo apt-get install com.qq.weixin.deepin
# QQ
sudo apt-get install com.qq.im.deepin
```

> 全部列表: https://deepin-wine.i-m.dev/

## 其他

其他配置的话也有很多,不过笔者之前已经有文章记录了,现在已经解决网络代理的问题了所以访问博客应该也没有问题了

- [git的SSH](https://luzhixing12345.github.io/2022/04/29/git/git%E7%9A%84SSH%E8%BF%9E%E6%8E%A5/)

  username email

- [切换NVIDIA显卡驱动](https://luzhixing12345.github.io/2022/11/28/%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE/Ubuntu%E5%88%87%E6%8D%A2NVIDIA%E9%A9%B1%E5%8A%A8/)

连接服务器的SSH免密配置一下

然后切一下双系统默认Windows,笔者电脑是DELL,使用F2进入的是bios的设置,F12进入的是boot menu.这里就是用F2进入bios把windows的调到ubuntu前面即可

## 英文环境

```bash
sudo apt install language-pack-en
sudo vim /etc/default/locale
```

在结尾添加内容

```txt
LANG="en_US.UTF-8"
LC_MESSAGES="C"
```

更新本地化设置

```bash
sudo update-locale
```

## 用户权限

添加一个用户, 拿到 sudo 权限

```bash
sudo adduser kamilu
sudo usermod -aG sudo kamilu
```

## 参考

- [Linux代理配置](https://luzhixing12345.github.io/2022/11/08/%E5%B7%A5%E4%BD%9C%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE/Linux%E4%BB%A3%E7%90%86%E9%85%8D%E7%BD%AE/)
- [windows下v2rayN+wsl2代理配置](https://luzhixing12345.github.io/2022/10/23/%E5%B7%A5%E4%BD%9C%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE/WSL2%E4%BB%A3%E7%90%86%E9%85%8D%E7%BD%AE/)
- [Ubuntu22.04安装Fcitx5中文输入法(详细)](https://zhuanlan.zhihu.com/p/508797663)
- [ubuntu 22.04 安装 微信/QQ](https://blog.csdn.net/weixin_38493195/article/details/124870781)