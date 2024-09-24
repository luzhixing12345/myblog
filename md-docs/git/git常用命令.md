---
title: git常用命令
date: 2022-07-15 22:56:19
tags: git
---

# git常用命令

> 相关解释 :
>
> - `BRANCH_NAME` : 分支的名字
> - 默认远程仓库的地址名称为 origin

- 删除远程分支

  ```bash
  git push origin --delete {BRANCH_NAME}
  ```

- 修改本地remote

  ```bash
  git remote set-url origin {URL}
  ```

- 删除本地分支

  ```bash
  git checkout {ANOTHER_BRANCH}
  git branch -D {BRANCH_NAME}
  ```

- 分支重命名

  ```bash
  git branch -m {NEW_NAME}
  ```

- 拉取远程仓库某一分支

  ```bash
  git checkout -b {BRANCH_NAME} origin/{BRANCH_NAME}
  ```

- 拉取远程仓库某一分支到本地某一分支

  ```bash
  git pull origin master:{BRANCH_NAME}
  ```

Git error "object file ... is empty"?

[how can i fix the git error object file is empty/12371337#12371337](https://stackoverflow.com/questions/11706215/how-can-i-fix-the-git-error-object-file-is-empty/12371337#12371337)

先试一下

```bash
git pull
```

```bash
find . -type f -empty -delete -print
git fsck --full
tail -n 2 .git/logs/refs/heads/main
git show hash
```