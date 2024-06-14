---
title: 使用poetry发布python包
date: 2022-04-29 11:37:58
tags: python
---

## 引言

熟悉python的朋友一定安装过很多第三方库,python的强大之处不仅在于简洁优雅,还有很好的社区环境,有许多无私的开源贡献者编写了许多实用高效的第三方库,比如matplotlib,numpy之类,只要你想要python实现的功能,几乎都可以搜索找到对应的python包,只需简单的pip安装,阅读相关文档了解其基本函数使用方法就可以迅速上手了,比起其他语言来说解决问题不可谓不快.

那么如果说我也希望为python的社区做出一些贡献,我能否开发一个python包用于实现一些功能呢? 当然是可以的,而且python社区十分欢迎你参与其中,为开源做出一份贡献.

## PYPI

那么如何去做呢? 显然在正常使用时如果我们编写了一个python的包(下假定该包名为lytorch),那么我们只需要在其同级目录下import lytorch即可使用,但是我们希望在所有位置都可以使用,在所有地方都可以使用,所有人都可以使用,那么显然我们需要将其移动到一个其他的位置,并且可以被引用到.

PYPI是一个很好的平台,全称为Python Package Index,是一个开源的python包管理的网站,我们只需要将我们编写好的代码上传到PYPI上,接着通过pip install命令安装,这样包就被下载到 `Lib/site-packages`下了,使用import之时可以在sys.path中搜索到这个路径,找到lytorch的包,就可以成功的使用了.

## 准备与发布

### 首先注册一个PYPI账号-[PYPI](https://pypi.org/)

注册成功之后回到主界面,右上角就是你的用户名,你将以这个身份进行登录

![20220429120333](https://raw.githubusercontent.com/learner-lu/picbed/master/20220429120333.png)

中间的搜索框中你可以找到所有发布在PYPI的包名,试试搜索 `matplotlib` `pyautogui` `numpy`

右上角进入个人project,目前没有任何项目.但是PYPI非常贴心的提供了很完整的教学文档,说明文档.如果你更倾向于阅读官方文档也可以移步至[PYPI上传包](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

## [poetry](https://python-poetry.org/)

如今2023年了已经不是setup.py的年代了,许多便利的工具可以帮助我们迅速的开发,构建,发布.这里主要介绍一下我个人倾向的poetry

> https://python-poetry.org/

poetry的使用非常简单,首先安装

```bash
pip install poetry
```

接下来你可以在一个新目录创建

```bash
poetry new poetry-demo
```

也可以在当前目录下创建

```bash
poetry init
```

通常来说我推荐先创建一个GitHub仓库初始化一些信息,然后通过git clone把仓库拉取到本地,再使用poetry init初始化,这样poetry可以根据.git信息完成一部分初始化内容

初始化的部分包括

- name: 包名
- version: 版本
- description: 描述信息
- License: 开源协议
- authors: 作者
- dependenciese: 依赖

初始化之后可以得到 `pyproject.toml` 文件,我们可以在之后修改这个文件以增加相关信息

这里需要注意的是,包名需要选择一个独一无二的,和PYPI已有的项目包名都不相同的包名.你可以在[PYPI](https://pypi.org/)中查询包名以确定是否已经存在,如果存在则需要重新想一个新名字,否则无法发布

## 依赖

接下来我们看一下依赖信息 `dependencies`

这里的依赖是指包的环境,比如下方的包的依赖指安装此包需要 python3.7, PyYAML6.0, MarkdownParser0.1.3

例如你的库依赖了numpy,你可以使用 poetry add numpy将其添加到你的包依赖中,当然你也可以手动添加

```txt
[tool.poetry.dependencies]
python = "^3.7"
PyYAML = "^6.0"
MarkdownParser = "^0.1.3"
```

除此之外简要说明一下后面的版本号:版本号分为三个部分: `主版本号.次版本号.修复版本号`

- 主版本号是一个大版本的更迭,一般意味着通用稳定的一个大版本,API的大型调整,架构的变化等等.
- 次版本号是一个相对更小的,稳定的版本,通常为修复了一些bug之后暂时维持稳定的一个状态版本
- 修复版本号就是遇到bug,修复bug,改进代码增加功能的一些版本发布和更新

日常在开发的时候在依赖中常常使用 `^` `~`

- ^: 指匹配最新的大版本依赖包，比如^1.2.3会匹配所有1.x.x的包，包括1.3.0，但是不包括2.0.0
- ~: 指匹配最近的小版本依赖包，比如~1.2.3会匹配所有1.2.x版本，但是不包括1.3.0
- *: 安装最新版本的依赖包

建议使用~来标记版本号，这样可以保证项目不会出现大的问题，也能保证包中的小bug可以得到修复

## 构建与发布

这里以笔者的一个库: [zood](https://github.com/luzhixing12345/zood) 为例

你需要在同级目录下创建一个文件夹zood, 这个文件夹不必须与zood同名,也可以叫做其他的名字(比如zoood).这里的区别是下载使用的 `pip install zood` 是你的包名,但是使用的时候`import 比如zoood`是你的这个文件夹的名字

这个文件夹必须含有一个 `__init__.py` 文件用于提供对外的引用接口,不在其中显示导出的是无法被外部引用到的.

zood目录内部的所有目录也是同理,每一级目录如果想要被外部作为库来引用,都需要创建 `__init__.py` 并在其中import对应的接口

构建使用

```bash
poetry build
```

发布你的python包需要首先获取API token, 前往 https://pypi.org/manage/account/ 创建一个 API token

![20230108135005](https://raw.githubusercontent.com/learner-lu/picbed/master/20230108135005.png)

使用如下命令替换 `my-token` 以配置密钥

```bash
poetry config pypi-token.pypi <my-token>
```

发布

```bash
poetry publish
```

接下来你就可以在PYPI上看到你的包了,所有人都可以下载使用!这很令人兴奋不是么?

## 命令行

poetry也提供了非常简单的命令行调用方式, 只需要在 pyproject.toml 中添加

```txt
[tool.poetry.scripts]
zood = 'zood.main:main'
```

这里表示当在命令行中输入 zood 的时候,会调用 zood.main 的 main 函数
