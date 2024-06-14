---
title: nodejs安装
date: 2024-02-11 12:12:12
tags: 环境配置
---

# nodejs安装

> npm 安装依赖的时候发现过期了(版本更新的真快啊), 记录一下流程

前往 [nodejs download](https://nodejs.org/en/download/) 安装新版 nodejs

安装在 `D:\nodejs`

```bash
node -v
```

进入 nodejs/ 并新建 `node_global` 和 `node_cache` 目录, 以防把垃圾安装在 C 盘

```bash
npm config set prefix "D:\nodejs\node_gobal"
npm config set cache "D:\nodejs\node_cache"
```

讲 `D:\nodejs\node_gobal` 加入环境变量

## 换源

原先的淘宝源失效了

```bash
npm install -g pnpm
```

```bash
npm config set registry https://registry.npmmirror.com

pnpm config set registry https://registry.npmmirror.com
```

## 参考

- [NodeJs安装与全局配置](https://blog.csdn.net/liu_shi_jun/article/details/80957335)
- [npm ,yarn 更换使用国内镜像源,阿里源,清华大学源](https://blog.csdn.net/ichen820/article/details/135747004)