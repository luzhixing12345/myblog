---
title: git的branch和pull
date: 2022-04-29 15:47:52
tags: git
---

> git官方提供了十分详细的描述,有很多直观的图片描述,很容易理解
>
> 我将在这部分根据我的理解给出一些描述性的图片,git的图片很好我并没有打算超越,仅作为学习记录
>
> [git官方的分支介绍](https://git-scm.com/book/zh/v2/Git-%E5%88%86%E6%94%AF-%E5%88%86%E6%94%AF%E7%AE%80%E4%BB%8B)
>
> Note: “origin” 并无特殊含义
>
>远程仓库名字 “origin” 与分支名字 “master” 一样，在 Git 中并没有任何特别的含义一样。 同时 “master” 是当你运行 git init 时默认的起始分支名字，原因仅仅是它的广泛使用， “origin” 是当你运行 git clone 时默认的远程仓库名字。 如果你运行 git clone -o booyah，那么你默认的远程分支名字将会是 booyah/master。

## pull | branch

这个过程我用一个实例来演示,希望有助于理解

- 首先我创建了一个新的GitHub仓库(git branch),新建了一个文件夹并将他们remote连接,创建README文件并且提交上去,其过程无二致

  ![20220324235742](https://raw.githubusercontent.com/learner-lu/picbed/master/20220324235742.png)

- 接着我补充了一些文件信息,创建`text.txt`,写入一句话,补充readme,作为第二次提交
  
  ![20220325000119](https://raw.githubusercontent.com/learner-lu/picbed/master/20220325000119.png)

  ![20220325000020](https://raw.githubusercontent.com/learner-lu/picbed/master/20220325000020.png)

- 截至目前,我已经在本地做了两次修改,并且全部提交到了GitHub上面,在GitHub中可以点击commit查看所有的提交记录

  ![20220325000249](https://raw.githubusercontent.com/learner-lu/picbed/master/20220325000249.png)

如果只有我一个人的话,我只需要每次写完代码commit,也可以多次commit保存记录选取最后一次push到GitHub,这样我的GitHub和本地仓库一定是统一的且是最新的

master分支不断前进,HEAD代表你目前所在分支也不断前进,同时你的本地仓库与远程仓库处于同一位置

![20220325000832](https://raw.githubusercontent.com/learner-lu/picbed/master/20220325000832.png)

![20220325001333](https://raw.githubusercontent.com/learner-lu/picbed/master/20220325001333.png)

但是如果是多人合作编写程序的话,这样面临的一个问题是可能是你在本地做了一些工作,但是已经有人提前把工作推送到GitHub上,这就导致远程仓库的master接受了新的push,但是你的本地依然维持原样,当你编写完毕想要push你的commit时发现有错误信息

- 我在GitHub中手动修改README文件并且提交
  
  ![20220325001904](https://raw.githubusercontent.com/learner-lu/picbed/master/20220325001904.png)

- 同时我也在本地修改README文件并且提交

  ![20220325002004](https://raw.githubusercontent.com/learner-lu/picbed/master/20220325002004.png)

这时产生了报错信息,即拒绝了我的提交,因为我的current branch is behind(我被落下了)

```git bash
luzhi@LZX MINGW64 /g/learner_lu/git-branch (master)
$ git push origin master
To github.com:learner-lu/git-branch.git
 ! [rejected]        master -> master (non-fast-forward)
error: failed to push some refs to 'github.com:learner-lu/git-branch.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. Integrate the remote changes (e.g.
hint: 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

git的推荐信息是使用`git pull`

- 我们使用`git pull`拉取对应仓库的对应分支

  ```git bash
  git pull origin master
  ```

`git pull`命令是将远程仓库与本地仓库进行统一,这里会出现一个问题: 如果是别人新建的文件,那么直接会在我的本地仓库复制;但如果是对于一个文件我也做了修改他也做了修改,这时就会产生冲突,因为不清楚这里的修改怎么做,需要手动解决冲突

![20220325002918](https://raw.githubusercontent.com/learner-lu/picbed/master/20220325002918.png)

vscode插件提供了方便的比较视图,可以选择接受现在的,接受当前提交到GitHub中最新的,还是都接受.解决所有冲突之后就可以commit了

```git bash
git commit -am "solve crash"
```

这种先pull后push的方式可以有效避免代码不同步,严格的commit检验保证了所有人的代码再提交的那一刻一定是与远程仓库的代码同步的,最新的. 但是于此同时也带来了一个问题,那就是每次我都需要处理冲突的文件,进行手动的选择接受哪一种修改,这显然不是一个好的方式,如果我交上去的东西被别人pull下来修改了,然后他把他的push上去. 那我再pull的时候又会发现不同,这显然不利于团队开发.

我们倾向于选择一种方式分开不同的开发,比如合理的分工,模块化到不同的文件夹/文件编写代码,这样就不需要处理冲突. 因为如果你没有改动这个文件夹/文件,其他人的修改会直接覆盖/更新此文件而不需要处理冲突(Fast-forward)

显然git也想到了这一点,比起创建文件夹这种本办法,git采用了分支的这种思想

- 我们可以创建一个新的分支`dev`,并且移动到这个分支
  
  ```git bash
  git branch dev
  git checkout dev
  ```

如果你在这个`dev`分支上做开发,比如新建了一些文件,改写了一些代码,提交了commit.这些操作都不会影响之前的master分支.

如果你现在选择移动到master分支 `git checkout master`,你会发现所有的dev中的修改全都不见了,仍然是创建dev时的样子,你可以继续在master中做开发.

当你master处理完毕后可以再回到dev分支,这时又回到了dev分支的状态,这种分支的切换对于处理不同任务等复杂的场景十分适合

> 注意: 切换分支前应commit所有修改项

对于多人开发时,可以创建多个分支以供不同contributer开发,最后再合理的时刻进行合并,或者更新主分支master

## fetch merge

常规情况使用pull操作即可强制更新本地仓库,还可以使用`git fetch` `git merge`来进行合并

> [pull与fetch的区别](https://blog.csdn.net/weixin_41975655/article/details/82887273)

简单来说就是`git fetch`不更新master只更新origin/master,然后使用`git merge`合并本地master和origin/master,产生新commit提交.

```git bash
git fetch origin
git merge origin/master
git commit -am "successfully merge"
git push origin master
```

`git pull`就是直接合并了本地master和本地remote

两者的本质区别就是`fetch`只是将远程仓库替换本地的remote,并不会修改你当前的任何文件,你可以检查fetch的内容再决定要不要合并.
而`pull`则直接进行合并,需要你现在处理冲突,决定是否改变文件.

普遍推荐使用`git fetch + git merge` 而不是 `git pull`,当然对于小项目来说看起来`git pull`更方便一些,也没有什么大问题

## rebase 变基

由dev变基到master

```git bash
git checkout dev
git rebase master
```

> 它的原理是首先找到这两个分支(dev master)最近共同祖先，然后对比当前分支(dev)相对于该祖先的历次提交，提取相应的修改并存为临时文件， 然后将当前分支指向目标基底 master, 最后以此将之前另存为临时文件的修改依序应用

rebase会确保在向远程分支推送时能保持提交历史的整洁.例如向某个其他人维护的项目贡献代码时。 在这种情况下，你首先在自己的分支里进行开发，当开发完成时你需要先将你的代码变基到 origin/master 上，然后再向主项目提交修改。 这样的话，该项目的维护者就不再需要进行整合工作，只需要快进合并便可。

> [一些其他变基过程](https://git-scm.com/book/zh/v2/Git-%E5%88%86%E6%94%AF-%E5%8F%98%E5%9F%BA)

也可以直接使用`pull + rebase`的方式,快速拉取变基合并. 如果有冲突需要处理冲突,选择接受哪一种修改(见git.md).

> [git rebase(master|REBASE 1/1)](https://blog.csdn.net/weixin_43845059/article/details/119754972)
>
> [git push: failed to push some refs to](https://blog.csdn.net/rocling/article/details/82956402)

```git bash
git pull --rebase origin master
```
