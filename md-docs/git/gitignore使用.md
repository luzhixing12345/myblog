---
title: gitignore使用
date: 2022-04-29 15:51:17
tags: git
---

> [Github官方.gitigore规范](https://github.com/github/gitignore)

.gitignore文件用来剔除不希望git上传的文件,包括

- 编译的中间文件
- 不重要的文件
- 一些项目运行阶段生成的文件
- 一些大文件(超过git默认的100M)

如果使用了`Commitizen`作为代码规范commit,我的个人`.gitignore`配置如下

```shell
/node_modules/
.vscode
CHANGELOG.md 
*.json
```

同时可以使用GitHub官方提供的不同语言的gitignore文件,创建仓库是可以直接选择gitignore文件

.gitignore文件通常需要根据具体的项目目录文件进行调整,需要自建`.gitignore`文件以定向剔除,也可以在多个文件夹下建立`.gitignore`

值得一提的是,gitignore中新加入的项并不会从已上传的仓库中删除,也就是说如果你已经上传了cpp文件后在gitignore中去除*.cpp,已上传的cpp并不会被删除.这是因为在暂存区拥有该文件的备份,使用`git add`命令如果文件未修改则直接使用备份,使gitignore生效的方法如下

- 稍微改动当前文件,空格/换行
- 清除暂存区的cached之后`git add`即可
  
  ```shell
  git rm -r --cached .
  git add .
  ...
  ```

GitHub并不支持上传空文件夹,这个其实算是git设计时的失误,[原回答](https://git.wiki.kernel.org/index.php/GitFaq#Can_I_add_empty_directories.3F),可以使用gitignore或者readme占位

```shell
Can I add empty directories? 
---
目前，Git索引（staging area）的设计只允许列出文件，
没有人有足够的能力进行更改以允许空目录，也没有人足够关心这种情况来纠正它。

在目录中添加文件时会自动添加目录。也就是说，目录不必添加到存储库中，也不需要单独跟踪。

你可以说“git add<dir>”，它会将文件添加到其中。

如果你真的需要一个目录存在于签出中，你应该在其中创建一个文件。
gitignore可以很好地实现这一目的（还有一个使用.NET framework的工具MarkEmptyDirs，
它允许您自动完成这项任务）；您可以将其留空，或填写不希望出现在目录中的文件名。
```

GitHub本身是不建议仓库体积很大的
