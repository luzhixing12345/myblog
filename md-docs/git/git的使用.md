---
title: git的使用
date: 2022-04-29 15:38:45
tags: git
---

由于笔者水平有限,该文档并不是git的教学文档,仅为学习了git的用法之后的总结,希望能通过整理的方式加深印象,如果对git尚不熟悉,可以参考以下文章

## Git入门级参考文章

>[git官方文档](https://git-scm.com/book/zh/v2)
>
>[知乎文章](https://www.zhihu.com/question/28976652/answer/1969388194)
>
>[知乎文章](https://zhuanlan.zhihu.com/p/135183491)
>
>[github markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
>
> [git电子书](https://github.com/luzhixing12345/luzhixing12345.github.io/releases/download/v0.0.1/progit.pdf)

## git的使用

git支持linux的部分命令,包括`cat`,`mkdir`,`touch`,`vim`,`rm`,`cd`等等,也有一些常用的命令和提交格式

git不支持完整的正则表达式语法(regex es),它只支持`unix fnmatch`(filename pattern matching),通常来说在命令行中使用正则语法容易出现误导，如`demo.c`等习惯性的写法,因此采用[unix的匹配写法](https://docs.python.org/3/library/fnmatch.html),具体为:

- `*`匹配任意字符,任意次数
- `?`匹配任意字符,一次
- `[seq]` 匹配 `seq` 中出现的字符,一次
- `[!seq]` 匹配不在 `seq` 中出现的字符,一次

如匹配 `demo.cpp`可使用如下任意一种写法,正则写法如 `\w*\.\w*` 将**不被识别**

```shell
*.cpp | demo.* | demo.???
```

当您使用 `Git` 和 `GitHub` 协作处理项目时，例如，如果您在 `Windows` 计算机上工作，并且您的合作者在 `macOS` 中进行了更改，则 `Git` 可能会产生意外的结果.您可以将 Git 配置为自动处理行尾，以便与使用不同操作系统的人员进行有效协作。

```shell
git config --global core.autocrlf true
```

### 关于 `add`

> 将文件从工作区 `add` 到暂存区

- **添加所有文件**

  ```shell
  git add .
  ```

- 添加所有 `.c`

  ```shell
  git add *.c
  ```

- **添加 `FILEPATH` 文件夹下所有的文件**

  ```shell
  git add FILEPATH/
  ```

- 查看添加了哪些文件

  ```shell
  git status
  ```
  
### 关于 `rm`

> 有时候添加错误的或未完成需要修改的文件到暂存区,需要从暂存区删除该文件

- **删除方式**
  > 注意,这里可以使用 `fnmatch`匹配文件名,但是如果某一匹配项不在暂存区而在工作区未被加入,则删除失败
  >
  > 例如 `1.txt` 在暂存区中, `2.txt` 未加入暂存区,则使用 `git rm --cached *.txt` 会删除失败
  >
  > `git add` 不会有这个问题,可以理解为把所有匹配项都加入暂存区,重复的再加一次

  - 从暂存区删除该文件,物理文件不删除(推荐使用),放入垃圾桶

    ```shell
    git rm --cached FILENAME
    ```

  - 删除暂存区中的文件和物理文件,**谨慎使用**

    ```shell
    git rm --f FILENAME
    ```

- 删除已提交的文件夹或文件
  
  ```shell
  git rm -r --cached FOLDER
  git add .
  ...
  ```

- 误删文件恢复 **git rm 需谨慎!!!**

  - 如果处于未提交状态
  
    ```shell
    # 查看所有修改项
    git reset 
    # 将FILENAME文件恢复
    git checkout FILENAME
    ```
  
  - 如果已经commit,那么会有些麻烦,只能退回上个版本,然后把被删除文件再找回来

    ```shell
    git reset HEAD^
    git checkout (捡垃圾)
    ```

### 关于 `commit`

> 将暂存区的文件上传到仓库区

- **提交**

  `-m`参数是一个较为常用的参数,用于将提交信息与命令放在同一行

  ```shell
  git commit -m "COMMIT MESSAGE"
  ```

  通常来说用于描述的commit信息应该记录更新了什么内容等等,一般来说一行足以.如果需要很多文件信息也可以使用

  ```git bash
  git commit
  ```
  
  打开commit信息文本,书写详细内容,使用方式同`vim`

- 查看commit日志(Q退出)

  ```shell
  git log
  ```

- 单行查看commit日志,关键信息

  ```shell
  git log --pretty=oneline
  ```

- 回退到上一个版本(`--hard`本地代码改变.**谨慎使用**)

  ```shell
  git reset --hard HEAD^
  ```

  回退到上N个版本

  ```shell
  git reset --hard HEAD~N
  ```

  > 通常来说使用 `git reset --hard HEAD^`来进行版本回退是因为有人错误的提交了commit,如提交到了不同的分支(branch)或者误修改了某些文件,但这种情况还是相对较少
  >
  > 这里提供两种可能会遇到的情况:
  >
  > 比如说你今天打算改一改代码,你可以先把所有文件`git add`然后`git commit`一次,然后开始修改,`a.txt b.txt c.txt`等文件,修改完之后你发现测试的结果不尽如人意,或者你觉得你的修改太愚蠢了太繁琐了想要重写,这时候就可以使用`git reset --hard HEAD` 来回到最后一次commit的位置,这样你在`a/b/c.txt`中的所有修改都会撤回(**注意会改变本地文件,使用时请注意**),就不需要你记住修改了什么文件再一次次`ctrl+z`回退了.
  >
  > 或者如果你改了某几个文件的代码,但是想撤回某一个文件的所有修改,可以使用 `git checkout -- FILENAME`来撤销修改
- 返回到某一个指定的版本

  ```shell
  git reflog                # 查看所有commit记录,根据commit内容搜索,找到前面对应的序号
  git reset --hard 3f72bae  # 同步到某一版本
  ```

### 关于 `push`

>将仓库区的文件上传到GitHub
>
>有时候会出现`Failed to connect to github.com port 443 after xxx ms: Timed out`的报错信息或者`OpenSSL fail`的报错,网上的解决方法很多,有时成功有时不成功,我搜集到的所有解决方法.目前使用SSH可以无压力的上传下载使用git

**Git保存的并不是文件的变化差异,而是文件不同时刻的快照**.

- `git add`操作是将文件加入暂存区,Git会为每个对象计算校验和(SHA-1哈希算法),保存blob对象的快照
  
  ![20220323201925](https://raw.githubusercontent.com/learner-lu/picbed/master/20220323201925.png)

- `git commit`操作会单独计算每一个目录的校验和,使用多个树对象来保存blob对象的校验和,最后再计算树对象的校验和,生成一个提交对象,包含树对象的指针和所有提交信息

  ![20220323202744](https://raw.githubusercontent.com/learner-lu/picbed/master/20220323202744.png)

- 每次提交都会包含一个指向上次提交对象的指针

  ![20220323202913](https://raw.githubusercontent.com/learner-lu/picbed/master/20220323202913.png)

首先与远程仓库建立连接,有两种方式

- 直接从URL克隆仓库,默认将 `origin`设置为该仓库的地址
  
  ```git bash
  git clone URL
  ```

- 将本地文件夹与远程仓库连接,`origin`对应远程仓库的地址(需要新建GitHub仓库)

  ```git bash
  git remote add origin git@github.com:luzhixing12345/git-learning.git
  ```

可以使用`git remote -v`查看远程仓库的地址,一个本地仓库可以连接多个远程仓库

默认的分支是`master`,也就是说我们选择将我们目前commit的本地仓库提交到某一个远程仓库的某一个分支上,我们使用

```git bash
git push origin master
```

第一次提交的时候可以选择`git push -u origin master`追踪此分支,这样默认选择以后都提交到`origin`远程仓库的`master`分支,之后的提交可以省略参数

```git bash
git push
```

---
总结: 一套基本的git/GitHub的文件流如下

- 初次配置

  ```git bash
  git init
  git add .
  git commit -m "upload all the files"
  git remote add origin git@github.com:luzhixing12345/git-learning.git
  git push -u origin master
  ```

- 之后的所有修改

  ```git bash
  git add .
  git commit -m "update git learning and fix docs bugs"
  git push
  ```

以上的命令已经可以满足绝大多数个人的项目开发与维护了,但是往往还有一些其他的问题,比如多人合作编写代码,比如临时修复bug等任务

---

git设计了很好的分支系统和项目拉取合并的方式,这一部分也十分重要,但并不是必要掌握的

接下来会介绍`branch | pull | fetch | merge`.这一部分可以说是git使用时最常见的问题,涉及多人合作完成项目,分支的使用|合并

### 优质网站

- [GitHub文件代理加速下载服务](https://ghproxy.com/)  (GitHub 文件/Releases/archive/gist/raw.githubusercontent.com)
