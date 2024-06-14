---
title: Ubuntu切换NVIDIA驱动
date: 2022-11-28 19:11:24
tags: 环境配置
---

笔者使用 Ubuntu22.04 出现了卡死的情况,且网上提到的解决办法均不奏效

> 其他解决办法: https://blog.csdn.net/qq_39779233/article/details/114758689

所以参考文章: https://blog.csdn.net/weixin_38890593/article/details/124795412 决定更换显卡驱动, ubuntu 默认使用nouveau显卡驱动,安装NVIDIA的显卡驱动

1. 下载显卡驱动

   首先需要电脑是N卡,可以通过如下命令查看显卡型号,笔者这里是笔记本的3060

   ```bash
   lspci |grep -E "VGA|3D"
   ```

   ![Screenshot from 2023-01-03 09-43-10](https://raw.githubusercontent.com/learner-lu/picbed/master/Screenshot%20from%202023-01-03%2009-43-10.png)

   进入 https://www.nvidia.cn/geforce/drivers/

   根据电脑显卡型号下载对应的驱动安装包,这里笔记本是notebook

   ![Screenshot from 2023-01-03 09-48-25](https://raw.githubusercontent.com/learner-lu/picbed/master/Screenshot%20from%202023-01-03%2009-48-25.png)

   下载之后修改文件的权限

   ```bash
   chmod +x /path/to/NVIDIA-Linux-*.run
   ```

2. 根据文档执行,这里以 Ubuntu 的情况为例,如果是 Debian and Linux Mint 需要根据文档修改

   https://www.if-not-true-then-false.com/2021/debian-ubuntu-linux-mint-nvidia-guide/

   进入root用户

   > 如果是vmware的话是不能su的,需要先sudo passwd root改一下密码(可以相同),然后以后就可以了

   ```bash
   sudo -i
   apt update
   apt upgrade
   apt autoremove $(dpkg -l xserver-xorg-video-nvidia* |grep ii |awk '{print $2}')
   apt reinstall xserver-xorg-video-nouveau
   reboot
   ```

3. 重启之后

   ```bash
   sudo -i
   apt install linux-headers-$(uname -r) gcc make acpid dkms libglvnd-core-dev libglvnd0 libglvnd-dev dracut
   echo "blacklist nouveau" >> /etc/modprobe.d/blacklist.conf
   ```

   修改grub配置文件

   ```bash
   vim /etc/default/grub
   ```

   修改配置文件

   ```txt
   GRUB_CMDLINE_LINUX_DEFAULT="quiet splash rd.driver.blacklist=nouveau"
   ```

   ```bash
   update-grub2
   mv /boot/initrd.img-$(uname -r) /boot/initrd.img-$(uname -r)-nouveau
   dracut -q /boot/initrd.img-$(uname -r) $(uname -r)
   systemctl set-default multi-user.target
   reboot
   ```

4. 再次重启之后

   再次重启之后就失去了开机的图形界面,接下来的操作在命令行中执行

   ```bash
   sudo -i
   cd 进入下载的NVIDIA驱动的目录,浏览器下的话默认在 ~/Download
   ./NVIDIA-Linux-*.run
   ```

   然后一路ENTER确认就可以了

   这部分时间很短,结束之后重新回到命令行,这里要注意重新回到的命令行很小很小,在屏幕的左下角,你可以按下回车看到

   ```bash
   systemctl set-default graphical.target
   reboot
   ```

   安装完成

   ![Screenshot from 2023-01-03 10-25-47](https://raw.githubusercontent.com/learner-lu/picbed/master/Screenshot%20from%202023-01-03%2010-25-47.png)