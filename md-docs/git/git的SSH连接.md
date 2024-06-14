---
title: git的SSH连接
date: 2022-04-29 15:44:25
tags: git
---

## 不使用https连接,使用SSH连接(推荐)

> 以下案例中使用的邮箱是 `luzhixing12345@163.com` 你只需要替换为你自己的邮箱即可

- 创建SSH key

  ```shell
  ssh-keygen -t rsa -C "luzhixing12345@163.com"
  ```

- 默认路径保存,文件保存在 `c:/user/luzhi/.ssh`(Windows) 或者 `~/.ssh`(GNU/Linux)

  如果你需要创建多个SSH,比如远程连接多台服务器,Github+SSH,请手动设置不同的名字加以区分,比如 `id_rsa_server`,**SSH私钥不能共用,一对一连接**

- 不设置密码,跳过
- 然后会在上面的文件夹中生成`id_rsa`(私钥)和`id_rsa.pub`(公钥),**私钥不要泄露!**
- 打开Github->settings->SSH and GPG keys->new SSH key
- title随便起,将`id_rsa.pub`复制到下方

  ```bash
  cat ~/.ssh/id_rsa.pub
  ```

- 确定后不久会收到Github的邮件
- 在git bash中输入,注意就是`git@github.com`不是你的邮箱,该操作是将你的邮箱与github建立连接

  ```shell
  ssh -T git@github.com
  ```

  如果在这里出错显示需要输入git@github.com的密码则需要额外配置一下config文件

  在.ssh目录下新建一个config文件,目的是将SSH映射到443端口处. 配置完毕后再次重连

  ```txt
  Host github.com
    User luzhixing12345@163.com
    Hostname ssh.github.com
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/id_rsa
    Port 443
  ```

- yes
  >SSH协议采用由人工判断公钥的fingerprint是否可信的方式.当使用ssh命令连接服务器时,命令行会提示如下信息:
  >
  > The authenticity of host '168.30.9.213 (\<no hostip for proxy command\>) can't be established.
  RSA key fingerprint is 23:42:c1:e4:3f:d2:cc:37:1d:89:cb:e7:5d:be:5d:53.
  Are you sure you want to continue connecting (yes/no)?

- 如果出现Hi "用户名"! You've successfully authenticated, but GitHub does not provide shell access则设置成功
- **之后使用ssh的地址`git@github.com:xxx`而不是https的地址`https://github.com/xxx`**
- 可以使用 `git remote` 查看远程仓库,默认为空.
  - 查看远程仓库绑定的地址

    ```shell
    git remote -v
    ```

  - 如果已经添加`origin`,可以使用如下命令删除

    ```shell
    git remote rm origin
    ```

  - 添加GitHub仓库地址,注意添加的是SSH的地址

    ```shell
    git remote add origin git@github.com:learner-lu/git-learning.git
    ```

  - 然后就可以自由的push啦

    ```shell
    git push origin main
    ```

## 如果之前都可以很稳定的push,突然有一天报错ssl port22 timeout(tnnd坑死我了)

这时候一般都不是你的问题,可以重新尝试一下`ssh -T git@github.com`, 如果仍然连接失败,网上有些方法是说添加一个config文件,换成443端口,我本人亲测不好使

最后找了好久,发现是校园网....

换流量,就可以了......

## 其他解决方法(偶尔可以解决,偶尔出问题)

- 关掉代理(1)

  ```shell
  git config --global  --unset https.https://github.com.proxy 
  git config --global  --unset http.https://github.com.proxy 
  ```

- 关掉代理(2)

  ```shell
  git config --global --unset http.proxy
  git config --global --unset https.proxy
  ```

- UU加速器 | steam++
  
  见[B站视频介绍](https://www.bilibili.com/video/BV1Aq4y1q7hr?spm_id_from=444.41.0.0)


## 参考

- [SSH key配置](https://blog.csdn.net/qq_36667170/article/details/79094257)
- [SSH key配置教程](https://www.runoob.com/git/git-remote-repo.html)
- [SSH SSL HTTPS](https://www.jianshu.com/p/5e3f9dfd2cb4)
