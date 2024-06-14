---
title: vscode基本配置
date: 2022-05-19 03:14:31
tags: 杂
---

1. 添加snipplet

   在`settings.json`中添加如下设置启用markdown的snippets

   ```json
   {
    "[markdown]": {
      "editor.formatOnSave": true,
      "editor.renderWhitespace": "all",
      "editor.quickSuggestions": {
          "other": true,
          "comments": true,
          "strings": true
      },
      "editor.acceptSuggestionOnEnter": "on"
    }
   }
   ```

   我的基本markdown快捷键配置

   ```json
   {
	"create table": {
		"prefix": "table",
		"body": [
			"|$1|$2|",
			"|:--:|:--:|",
			"|||"
		],
		"description": "create table in markdown"
	},
	"create code snippet":{
		"prefix": "code",
		"body": [
			"```$1",
			"",
			"```"
		],
		"description": "create code snippet"
	},
	"create note info in my blog":{
		"prefix": "info",
		"body": [
			"{% note info %}",
			"$1",
			"{% endnote %}"
		]
	},
	"create note success in my blog":{
		"prefix": "suc",
		"body": [
			"{% note success %}",
			"$1",
			"{% endnote %}"
		]
	},
	"create note warning in my blog":{
		"prefix": "warn",
		"body": [
			"{% note warning %}",
			"$1",
			"{% endnote %}"
		]
	}
   }
   ```

2. 安装clangd

   vscode扩展,搜索clangd,安装.

   右下角弹出提示下载clangd,点击确定即可

   官网的地址在 https://clangd.llvm.org/, 如果没有代理可以根据系统参考[文档](https://clangd.llvm.org/installation)下载release

   如果文件中使用了部分头文件,添加方法为: 新建`.vscode/settings.json`

   其中 `-I` + 头文件目录即可, 编译的参数可以在这里指定. 如果gcc版本低可以使用指定使用clang编译器

   > 如果不需要c++17标准不需要加入`-std=c++17`

   ```json
   {
       "clangd.fallbackFlags": [
           "-I/root/X86",
           "-std=c++17"
       ],
       "clangd.arguments": [
           "--query-driver=/usr/bin/clang++", // 使用clang编译
           "--background-index", // 在后台自动分析文件(基于complie_commands)
           "-j=12",  // 同时开启的任务数量
           "--clang-tidy", // clang-tidy功能
           "--clang-tidy-checks=performance-*,bugprone-*",
           "--all-scopes-completion", // 全局补全(会自动补充头文件)
           "--completion-style=detailed", // 更详细的补全内容
           "--header-insertion=iwyu" // 补充头文件的形式
       ]
   }
   ```

   重启即可

3. clang-format

   ```bash
   sudo apt install clang-format
   ```

   ```bash
   clang-format -style=Google -i main.c
   ```

   > 使用clang-format -h 查看所有style

   > https://blog.csdn.net/softimite_zifeng/article/details/78357898

   下面贴一个我自己比较喜欢的clang-format

   ```txt
   BasedOnStyle: Google
   IndentWidth: 4
   AllowShortFunctionsOnASingleLine: None
   AllowShortBlocksOnASingleLine: Never
   AllowShortIfStatementsOnASingleLine: false
   BraceWrapping:
     AfterFunction: true
     AfterClass: true
     AfterControlStatement: false
     SplitEmptyFunction: false
     SplitEmptyRecord: false
     SplitEmptyNamespace: false
     BeforeCatch: true
     BeforeElse: true
     IndentBraces: true
     AfterFor: true
   ```

使用snippets屏蔽推荐词,并且使snippet的推荐置顶

```json
{
    "editor.wordBasedSuggestions": false,
    "editor.snippetSuggestions": "top"
}
```

## VS Code加载 Web 视图时出错

> [解决办法](https://blog.csdn.net/GMT_C/article/details/125405459)

```bash
code --no-sandbox
```
