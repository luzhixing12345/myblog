---
title: Windows PowerShell美化以及 Vscode 终端美化配置
date: 2023-02-28 17:12:12
tags: 环境配置
---

# Windows Powershell美化以及 Vscode 终端美化配置

效果展示

![20220704100352](https://raw.githubusercontent.com/learner-lu/picbed/master/20220704100352.png)

## 下载

首先我们配置 Powershell, windows本身的Windows powershell(蓝色的)操作系统自带的并不是我们需要的

微软推出了一个新的终端[terminal](https://github.com/microsoft/terminal),是一个跨平台的应用程序,界面与之前的terminal相同但是增加了一些功能

点进去之后有两种下载方式,一种是官方推荐的使用 microsoft store 下载, 另一种就是通过 releases 下载

![20220704100832](https://raw.githubusercontent.com/learner-lu/picbed/master/20220704100832.png)

我个人在microsoft store下载速度很慢,所以安装的最新的realses的版本,注意区分不同操作系统的版本,我是win11

![20220704100933](https://raw.githubusercontent.com/learner-lu/picbed/master/20220704100933.png)

安装之后就可以查看到一个终端预览,打开之后就是基本的界面,明显可以看出做了圆滑,在设置里面也多了许多功能

![20220704101132](https://raw.githubusercontent.com/learner-lu/picbed/master/20220704101132.png)

这里的windows powershell也并不是我们需要的,我们需要格外单独下载一个[powershell](https://github.com/PowerShell/PowerShell)

之后根据操作系统选择最新的版本就可以了,通常来说都是64位windows所以选择LTS版本的就可以了.

> 当然你也可以翻阅找到所有releases版本下载

安装之后就可以在开始界面看到多出了一个powershell7,这个就是我们今天的主角

![20220704101740](https://raw.githubusercontent.com/learner-lu/picbed/master/20220704101740.png)

点开之后还是熟悉的界面,没什么变化.

依次执行以下三条命令,他会为你安装 `oh-my-posh` 和 `posh-git` 两个模块

> 安装过程中全部选择 Y

```bash
Install-Module oh-my-posh -Scope CurrentUser -SkipPublisherCheck
Install-Module posh-git -Scope CurrentUser
Install-Module -Name PSReadLine -AllowPrerelease -Scope CurrentUser -Force -SkipPublisherCheck
```

之后导入模块

```bash
Import-Module posh-git
Import-Module oh-my-posh
```

在导入 `oh-my-posh` 中会弹出一段话, 大致意思是目前 oh-my-posh 更新了一个版本,不使用`Import-Module oh-my-posh` 来安装了,并提供了一个[网址](https://ohmyposh.dev/docs/migrating)

点击进入之后我们看到这是powershell的网址,说明了模块的更新和修改

![20220704102713](https://raw.githubusercontent.com/learner-lu/picbed/master/20220704102713.png)

阅读说明之后按照它的提示首先移除模块的缓存

```bash
Remove-Item $env:POSH_PATH -Force -Recurse
```

然后进入windows的[页面](https://ohmyposh.dev/docs/installation/windows),提示我们使用之前下载过的 windows terminal

接着执行

```bash
winget install JanDeDobbeleer.OhMyPosh -s winget
```

短暂的等待之后就安装完成了,本次更新为我们带来了`oh-my-posh.exe` 和旗下的所有主题 `themes`

## 主题选择

现在的powershell还是看起来没什么区别,我们可以选择一款喜爱的主题,执行命令查看所有主题

```bash
Get-PoshThemes
```

> 看花了眼的话可以在官网的[主题](https://ohmyposh.dev/docs/themes)页面查看所有主题,选择一个比较喜欢的主题吧,我个人选择的是`marcduiker`

接着配置主题,命令行中提示了我们如何设置

![20220704103853](https://raw.githubusercontent.com/learner-lu/picbed/master/20220704103853.png)

执行命令

```bash
oh-my-posh init pwsh --config C:\Users\luzhi\AppData\Local\Programs\oh-my-posh\themes/jandedobbeleer.omp.json | Invoke-Expression
```

当前使用的就是`jandedobbeleer`主题了,当然你可以选择你的主题名字,注意`luzhi`变成你的名字就好了

![20220704104026](https://raw.githubusercontent.com/learner-lu/picbed/master/20220704104026.png)

## 配置文件

看样子可以了,但是你会发现退出再重进又变成最开始的状态了,这时候我们需要设置一个配置文件让每一次运行都执行这条命令

```bash
notepad.exe $PROFILE
```

第一次执行会创建一个新的配置文件,之后在执行就是打开这个配置文件,将上面的命令复制到这里,保存.

之后每一次进入都是这个主题啦!

接着我们美化以下图标

```bash
Install-Module -Name Terminal-Icons -Repository PSGallery
Import-Module -Name Terminal-Icons
```

通过`ls`命令可以看到所有文件都根据它的属性有了不同的图标显示

![20220704104756](https://raw.githubusercontent.com/learner-lu/picbed/master/20220704104756.png)

再次使用 `notepad.exe $PROFILE` 也将 `Import-Module -Name Terminal-Icons` 加入其中作为默认启动项

最后我们再设置一下命令行的自动补全,执行命令

```bash
Import-Module PSReadLine
Set-PSReadLineOption -PredictionSource History
```

将以下内容添加到$profile结尾

```bash
# Shows navigable menu of all options when hitting Tab
Set-PSReadlineKeyHandler -Key Tab -Function MenuComplete

# Autocompletion for arrow keys
Set-PSReadlineKeyHandler -Key UpArrow -Function HistorySearchBackward
Set-PSReadlineKeyHandler -Key DownArrow -Function HistorySearchForward

# auto suggestions
Import-Module PSReadLine
Set-PSReadLineOption -PredictionSource History
```

最后你的配置文件应该和我的类似

```bash
oh-my-posh init pwsh --config C:\Users\luzhi\AppData\Local\Programs\oh-my-posh\themes/marcduiker.omp.json | Invoke-Expression
Import-Module -Name Terminal-Icons
# Shows navigable menu of all options when hitting Tab
Set-PSReadlineKeyHandler -Key Tab -Function MenuComplete

# Autocompletion for arrow keys
Set-PSReadlineKeyHandler -Key UpArrow -Function HistorySearchBackward
Set-PSReadlineKeyHandler -Key DownArrow -Function HistorySearchForward

# auto suggestions
Import-Module PSReadLine
Set-PSReadLineOption -PredictionSource History
```

可以看到补全和自动提示也出现了

![20220704170541](https://raw.githubusercontent.com/learner-lu/picbed/master/20220704170541.png)

我的主题对于不同的git状态的显示还是不错的

![20220704170757](https://raw.githubusercontent.com/learner-lu/picbed/master/20220704170757.png)

## 字体

这时候我们会发现一个奇怪的问题,我的主题为什么会有一些奇怪的白框框,当然你的主题可能没有.

出现这个问题的原因是你选择的主题使用了特殊的字体库 `Nerd Fonts`(书呆子字体),你没有安装这个字体库所以会出现乱码.如果主题没有使用这个字体库那么倒也没有问题

你可以在[字体库](https://www.nerdfonts.com/font-downloads)查看所有字体,我个人比较喜欢的是`CodeNewRoman Nerd Font`这款字体,新罗马字体我一直比较喜欢~

你可以直接点击下载,解压之后将压缩包里所有的字体文件点击安装.

ohmyposh也提供了一键下载,选择你的字体名字就可以下载了

```bash
oh-my-posh font install
```

现在你可以直接点击powershell来启动你的终端,我们也可以配置默认打开powershell,

![20220704110548](https://raw.githubusercontent.com/learner-lu/picbed/master/20220704110548.png)

![20220704110636](https://raw.githubusercontent.com/learner-lu/picbed/master/20220704110636.png)

选择你的字体,保存

![20220704110702](https://raw.githubusercontent.com/learner-lu/picbed/master/20220704110702.png)

重启就可以发现没有问题了

现在使用终端预览就可以直接打开一个带主题的powershell了,但是会需要先执行配置文件,会有一些卡顿.

## Vscode终端

打开终端选项然后下拉找到默认终端选择powershell

![20220704110956](https://raw.githubusercontent.com/learner-lu/picbed/master/20220704110956.png)

![20220704111102](https://raw.githubusercontent.com/learner-lu/picbed/master/20220704111102.png)

重启终端之后发现又出现了字体的问题

设置 -> font family 找到字体库,这里默认是空的,填入之前字体名字,然后补一个`monospace`

![20220704111226](https://raw.githubusercontent.com/learner-lu/picbed/master/20220704111226.png)

```bash
CodeNewRoman Nerd Font, monospace
```

这时候你会发现你文本编辑器中的字体也变了,没错,font family是所有的字体库,vscode的默认字体是Consolas,如果你想保持原先的字体,那么只需加在font family的最前面

```bash
Consolas, CodeNewRoman Nerd Font, monospace
```

大功告成了

![20220704111426](https://raw.githubusercontent.com/learner-lu/picbed/master/20220704111426.png)
