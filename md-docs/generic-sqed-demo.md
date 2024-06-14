---
title: generic-sqed-demo
date: 2023-07-20 09:10:14
tags: 形式化验证
---

# generic-sqed-demo 复现踩坑

## 前言

本文是针对 [generic-sqed-demo](https://github.com/upscale-project/generic-sqed-demo) 的复现过程记录, 作者提供了[docker](https://github.com/upscale-project/generic-sqed-demo#docker)快捷部署方式, 这里采用直接复现的方式, 工作环境: WSL2(Ubuntu22.04)

> 执行过程中存在诸多 git clone, curl 等需要下载外部资源的情况, 请确保网络通畅

Github 仓库地址: [generic-sqed-demo](https://github.com/upscale-project/generic-sqed-demo)

```bash
git clone git@github.com:upscale-project/generic-sqed-demo.git
cd generic-sqed-demo
```

本项目需要两个依赖, 分别是 [yosys](https://github.com/YosysHQ/yosys) 和 [pono](https://github.com/upscale-project/pono)

直接所在位置为当前根目录下

```bash
├── generic-sqed-demo
│   ├── SQED-Generator
│   ├── cadical
│   ├── docker
│   ├── libpoly
│   ├── pono                   # pono
│   ├── qed-wireup-patches
│   ├── ridecore-bugfix-patch
│   ├── ridecore-src-buggy
│   ├── sqed-generator
│   └── yosys                  # yosys
```

## yosys

作者提供了 `./setup-yosys.sh` 用于直接下载安装, 读者可先尝试执行此过程

```bash
sudo apt-get install build-essential clang bison flex \
	libreadline-dev gawk tcl-dev libffi-dev git \
	graphviz xdot pkg-config python3 libboost-system-dev \
	libboost-python-dev libboost-filesystem-dev zlib1g-dev
```

运行

```bash
# generic-sqed-demo/$
./setup-yosys.sh
```

如果出现问题, 可以克隆 [yosys](https://github.com/YosysHQ/yosys), 安装下面的依赖

选择编译器然后编译安装

```bash
make config-gcc
make
sudo make install
```

如果仍然存在问题可以选择直接采用包管理工具安装预编译的二进制文件

```bash
sudo apt install yosys
```

## pono

作者同样提供了 `./setup-pono.sh`

> 笔者没有运行, 采用了直接下载编译 [pono](https://github.com/upscale-project/pono) 的方式

pono 内部本身又需要了一些依赖, 不过好在作者也提供了一些快捷脚本, 首先安装一下 bison 和 flex

```bash
# generic-sqed-demo/pono/$
./contrib/setup-bison.sh
./contrib/setup-flex.sh
```

### smt-switch

作者提供了安装脚本 `./contrib/setup-smt-switch.sh` 但 smt-switch 本身也需要一些以来, 尤其是其中 cvc5, 再执行之前需要先安装一下必须的依赖

![20230720111732](https://raw.githubusercontent.com/learner-lu/picbed/master/20230720111732.png)

> pono/deps/smt-switch/cvc5/CMakeLists.txt

首先需要安装 GMP

> 参考 [Could NOT find GMP (missing: GMP_LIBRARIES GMP_INCLUDE_DIR)](https://github.com/PyMesh/PyMesh/issues/293)

```bash
sudo apt-get install libmpfr-dev libgmp-dev libboost-all-dev
```

接着安装 poly 的预编译版本

```bash
sudo add-apt-repository ppa:sri-csl/formal-methods
sudo apt-get update
sudo apt-get install libpoly-dev
```

或从源码编译 [libpoly](https://github.com/SRI-CSL/libpoly)

```bash
mkdir build
cmake .. -DCMAKE_BUILD_TYPE=Release
make
sudo make install
```

接着安装 [cadical](https://github.com/arminbiere/cadical), 只能从源码编译, 然后将其直接复制到系统路径下

```bash
./configure && make
cp libcadical.a /usr/lib/x86_64-linux-gnu/
```

最后检查一下环境中是否有 java

```bash
javac -version
```

如果没有安装 JDK JRE

```bash
sudo apt install default-jre
sudo apt install default-jdk
```

最后可以执行了

```bash
# generic-sqed-demo/pono/$
./contrib/setup-smt-switch.sh
./contrib/setup-btor2tools.sh
./configure.sh && cd build && make
```

## 结尾

如果至此, 那么恭喜你已经克服种种依赖难关

```bash
# generic-sqed-demo/$
./setup-sqed-generator.sh
./generate-qed-files.sh
./wire-up-qed-module.sh
./run-pono.sh
```

> 笔者这里的 yosys 运行会出现奇怪的报错, 问题是关于 qed-generator, 您也可以下载此处 [sqed.tar.gz](https://github.com/learner-lu/resources-download/releases/download/v0.0.1/sqed.tar.gz) 替换

![20230720113253](https://raw.githubusercontent.com/learner-lu/picbed/master/20230720113253.png)
