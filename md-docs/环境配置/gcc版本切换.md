---
title: gcc版本切换
date: 2023-03-14 14:55:15
tags: 环境配置
---

本文简单记录一下gcc版本的选择

在编译qemu的过程中提示gcc版本至少是7, 我个人的ubuntu使用的是16.04, 默认gcc5.4, 所以还需要更换一下gcc版本

```bash
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt-get update
sudo apt-get install gcc-8
```

安装完成之后可以看到已经有两个gcc版本了

```bash
ll /usr/bin/gcc*
```

![20230314135223](https://raw.githubusercontent.com/learner-lu/picbed/master/20230314135223.png)

接着设置各个gcc版本的优先级, 这里将gcc-8设置为最高优先级,即gcc默认调用的是gcc-8

```bash
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 80
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5 50

sudo update-alternatives --config gcc # 手动切换gcc版本
```

![20230314135601](https://raw.githubusercontent.com/learner-lu/picbed/master/20230314135601.png)
