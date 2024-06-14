---
title: 优雅的日志记录-logging
date: 2022-05-13 15:11:39
tags: python
---

## 前言

最近在写代码的过程中遇到了一些问题,如果我想输出一些信息,如果使用print函数的话,由于深度学习项目时间较长,我会将它提交到超算进行计算,但是它并不会实时输出,我必须要等到运行结束才能看到结果,如果一点有任何异常报错退出,那么我也看不到所有的print信息.

况且使用print是一种比较简单的输出格式,输出到控制台的话无法记录下来,如果使用txt单独保存信息似乎过于原始,我希望选择一种更加优雅的方式来记录信息,于是查阅资料后尝试使用了logging模块来记录信息,体验很好,分享给大家.

参考文章:

- [python3.7-logging模块](https://docs.python.org/3.7/library/logging.html?highlight=logging)
- [简书-logging模块使用教程](https://www.jianshu.com/p/feb86c06c4f4)
- [知乎-logging模块详解](https://zhuanlan.zhihu.com/p/425678081)
- [B站视频-<清晰详细>](https://www.bilibili.com/video/BV1sK4y1x7e1)
- [博客记录](https://www.cnblogs.com/kangshuaibo/p/14700833.html#%E6%88%91%E7%9A%84%E4%BD%BF%E7%94%A8%E6%96%B9%E5%BC%8F)

## logging模块简介

`logging`是python内置的模块,不需要下载就可以直接import使用

日志的等级分为五级

|日志等级|描述|
|:--:|:--:|
|DEBUG|基本的调试信息,可以用于输出一些特定位置的值用于调试程序|
|INFO|正常的信息,可以用于输出某些节点/阶段的信息|
|WARNING|警告信息,可以用于输出一些不合适的错误信息,比如输入不符合预期等等|
|ERROR|错误信息,一些严重的错误信息|
|CRITICAL|严重错误信息|

> 通常来说我们个人使用的话前三个日志等级应该就足够满足了

日志等级是从上到下,DEBUG等级的日志可以显示所有日志,CRITICAL等级就只能显示CRITICAL等级的.

```python
import logging

logging.debug("debug_msg")
logging.info("info_msg")
logging.warning("warning_msg")
logging.error("error_msg")
logging.critical("critical_msg")
```

输出结果是

```bash
WARNING:root:warning_msg
ERROR:root:error_msg
CRITICAL:root:critical_msg
```

可以看出来默认的logging等级是WARNING

我们可以使用`basicConfig`函数来调整日志输出的等级

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logging.debug("debug_msg")
logging.info("info_msg")
logging.warning("warning_msg")
logging.error("error_msg")
logging.critical("critical_msg")
```

输出结果是

```bash
DEBUG:root:debug_msg
INFO:root:info_msg
WARNING:root:warning_msg
ERROR:root:error_msg
CRITICAL:root:critical_msg
```

{% note info %}
这也给我们提供了一组思路,就是可以在编写程序的时候在一些位置使用DEBUG等级的日志,在某些关键节点使用INFO等级的日志作为阶段提示信息,在一些可能会需要获取用户输入的地方写入WARNING日志,在一些函数内部可以做一些判断,对错误信息打上ERROR日志,这样的话如果启用DEBUG等级的日志就可以查看到所有信息,如果没什么问题的话就使用INFO等级,只看到一些正常的阶段提示信息,**这样直接就忽略了所有的DEBUG的日志,也不用去像以前一样注释print函数**

如果程序出错,INFO等级的日志也可以看到ERROR或CRITICAL等级的错误,进行排查
{% endnote %}

## logging的进阶用法

接下来介绍logging模块的四个组件,初识这一部分的时候看文档看不太懂,后来还是看了视频的讲解对这几个组件的应用理解了很多,下面我尽可能使用平实的语言来介绍其使用方式

|组件名称|用途|
|:--:|:--:|
|Logger(记录器)|创建一个基本的日志的对象|
|Handlers(处理器)|将记录器产生的日志信息发送到目的地|
|Filter(过滤器)|定向过滤显示一些日志,不显示一些日志,相比level等级有了更高的控制精度|
|Formatter(格式化器)|控制输出格式|

这四个组件看起来不是特别好理解,一些文字描述似乎也有些云里雾里,下面我会通过一个实际的例子来介绍他们的使用方法

---

### 记录器Logger

我们先创建一个logger记录器,命名为`PYTHON-LOGGER`,然后将他的日志等级设置为DEBUG等级

```python
import logging
#创建记录器 （全局）
logger = logging.getLoger("PYTHON-LOGGER")
```

{% note info %}
值得一提的是,getLogger这个函数比较有趣,logging在定义了一个logger的名字之后,就会把这个记录器的相关信息保存起来,如果你在其他文件的位置(比如说另一个 `xx.py` 文件)中也使用了`logger = logging.getLogeer("PYTHON-LOGGER")`这样返回一个logger,他的信息与这个第一次定义过的完全相同,相当于是一个全局的变量
{% endnote %}

### 处理器Handler

接下来我们为这个记录器创建两个处理器(Handlers),一个用于把信息输出到控制台(console),一个用于把信息输出到日志文件(log file)

```python
import logging
import sys
#创建记录器 （全局）
logger = logging.getLoger("PYTHON-LOGGER")
logger.setLevel(logging.DEBUG)

#用于输出到控制台，使用StreamHandler的处理器
consoleHandler = logging.StreamHandler(stream=sys.stdout)
consoleHandler.setLevel(logging.DEBUG)

#用于输出到文件，使用FileHandler处理器
fileHandler = logging.FileHandler(filename='file.log',mode = "w")
# w表示覆盖之前的文件内容，也可以使用 "a" 来从文件结尾接着写
fileHandler.setLevel(logging.INFO)

#将处理器加入到记录器中
logger.addHandler(consoleHandler)
logger.addHandler(fileHandler)
```

{% note info %}
注意到我们给控制台的处理器设置了DEBUG等级,给文件处理器设置了INFO等级,也就是说现在的的fileHandler的日志等级更高,DEBUG的信息并不会输出到文件中

同时注意到我们也需要给logger设置日志等级为DEBUG,因为默认的logger等级是WARNING,日志等级是层级递进的,记录器->处理器,只会显示更高等级的日志信息,所以我们的处理器日志等级要比logger更高才会显示,所以设置logger为DEBUG等级(最低)
{% endnote %}

接下来我们可以简单的记录一些信息来看一看现在是什么情况.

```python
...
logger.debug("this is a debug message")
logger.info("this is a info message")
logger.warning("this is a warning message")
```

可以看到控制台输出了三条信息,文件夹中创建了一个`file.log`文件,其中记录了两条信息

`StreamHandler`和`FileHandler`是两个比较常用的处理器类型,处理器的任务是将日志文件内容发送到某一个位置,这两个处理器分别是发送到流和发送到磁盘文件,当然除此之外还有其他的[处理器函数](https://docs.python.org/3.7/library/logging.handlers.html#module-logging.handlers)

- `SocketHandler`可以使用Socket将日志记录发送到网络套接字,建立TCP连接发送到某一个IP地址
- `WatchedFileHandler`可以监视记录到的文件的类,如果文件发生更改，它将被关闭并使用文件名重新打开
- `TimedRotatingFileHandler`可以按特定时间轮换替换日志文件,比如说你需要一个长时间运行在服务器上的python程序,每天的日志文件可能会很大,它可以设置按天/按时间/日志文件定时分离保存等等操作.
- `SMTPHandler`可以将日志记录邮件发送到电子邮件地址
- `HTTPHandler`可以将日志记录消息发送到 Web 服务器

处理器的功能十分强大,基本标准库提供的处理器类型可以覆盖满足基本的日志需求. 当然作为个人使用的话其实用不到这么复杂的东西,我们使用控制台输出和文件记录两个日志处理器就可以满足我们debug文件的需求了,如果感兴趣的话可以了解一下

### 过滤器Filter

{% note info %}
这个说实话我觉得没啥用,一看一过得了
{% endnote %}

过滤器的作用是可以精细的区分记录器. 比如说我们设置了多个记录器,我们可以使用过滤器来特定的显示记录器的内容,而不显示某些记录器的内容

```python
import logging

logger1 = logging.getLoger("a")
logger2 = logging.getLoger("a.b")
logger3 = logging.getLoger("a.b.c")
logger4 = logging.getLoger("d.b.c")
logger5 = logging.getLoger("d.b")
logger6 = logging.getLoger("e.a")

filter = logging.Filter("a.b")
```

过滤器的操作是与python的包名类似的,该包和其子包都会被过滤掉,也就是说2,3logger会被过滤掉,不会被记录

### 格式化器Formatter

格式化器是一个很有用的东西,它可以用于控制输出的格式

默认的输出格式是很简单的 `DEBUG:root:debug_msg`,它由三部分组成,DEBUG表示日志等级level,root是默认的记录器名字,我们可以用是getLogger来改变它的名字,debug_msg是输出的信息

我们可以使用格式化器来输出我们想要的格式

```python
import logging
import sys
#创建记录器 （全局）
def main():
    logger = logging.getLoger("PYTHON-LOGGER")
    logger.setLevel(logging.DEBUG)

    #用于输出到控制台，使用StreamHandler的处理器
    consoleHandler = logging.StreamHandler(stream=sys.stdout)
    consoleHandler.setLevel(logging.DEBUG)

    #用于输出到文件，使用FileHandler处理器
    fileHandler = logging.FileHandler(filename='file.log',mode = "w")
    # w表示覆盖之前的文件内容，也可以使用 "a" 来从文件结尾接着写
    fileHandler.setLevel(logging.INFO)

    formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)7s] [%(filename)8s] [%(funcName)8s] [%(lineno)3d]: %(message)s", datefmt="%Y %m/%d %H:%M:%S")

    fileHandler.setFormatter(formatter)
    consoleHandler.setFormatter(formatter)

    #将处理器加入到记录器中
    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)

    logger.debug("this is a debug message")
    logger.info("this is a info message")
    logger.warning("this is a warning message")

if __name__ == "__main__":
    main()

```

{% note info %}
值得注意的是formatter是需要加在handler上面的
{% endnote %}

控制台的输出的结果是

```txt
[2022 05/14 00:48:31] [  DEBUG] [    demo.py] [    main] [ 29]: this is a debug message
[2022 05/14 00:48:31] [   INFO] [    demo.py] [    main] [ 30]: this is a info message
[2022 05/14 00:48:31] [WARNING] [    demo.py] [    main] [ 31]: this is a warning message
```

这是我比较喜欢的一种输出格式,我们可以设置时间,文件名,函数名,行号等等,还可以输出线程,进程,路径等等[更多信息](https://docs.python.org/3.7/library/logging.html?highlight=logging#logrecord-attributes),不过对于我来说并不需要那么多

{% note success %}
当你创建了一个logger并给了它一个名字之后(通常是项目名),你可以再次调用这个logger而不需要重新配置信息,比如再次使用getLogger("PYTHON-LOGGER")后使用logger.info记录日志,日志的保存方式依然和原先相同
{% endnote %}

## logging的工程化用法

上述的方式已经可以基本完成需求了,但是我们可以有一种更加优雅的方式,使用配置文件.

新建一个logging.conf文件,将如下信息填入

> conf文件暂不支持中文字符,否则读取的时候会出现gbk错误,所以注释都是英文写的

```python
#./logging.conf

# set a logger, root is must
[loggers]
keys=root,PROJECT

# two handler, file and consolehandler
[handlers]
keys=fileHandler,consoleHandler

# formatter, declear below
[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_PROJECT]
level=DEBUG 
handlers=fileHandler,consoleHandler
qualname=PROJECT_NAME
# often choose propagate=0
propagate=0

[handler_consoleHandler]
class=StreamHandler
args=(sys.stdout,)
level=DEBUG
formatter=simpleFormatter

# use TimeRotatineFileHandler is more professional
[handler_fileHandler]
class=handlers.TimedRotatingFileHandler
# record after 3600s of midnight -> 1:00, 0 means save all the previous files
args=('PROJECT_NAME.log','midnight',3600,0)
level=DEBUG
formatter=simpleFormatter

[formatter_simpleFormatter]
format=[%(asctime)s] [%(levelname)7s] [%(filename)8s] [%(funcName)8s] [%(lineno)3d]: %(message)s
datefmt=%Y %m/%d %H:%M:%S
```

这样一个配置文件的内容就完成了,我们省去了写代码的时间,直接可以通过读取配置文件来得到一个logger

```python
import logging
import logging.config

logging.config.fileConfig('logging.conf')

logger = logging.getLogger('PROJECT_NAME')
logger.debug("This is PROJECT logger, debug")

logger.info("hello world")
```

运行结果

```txt
[2022 05/14 09:07:47] [  DEBUG] [    b.py] [<module>] [  7]: This is PROJECT logger, debug
[2022 05/14 09:07:47] [   INFO] [    b.py] [<module>] [  9]: hello world
```

接下来以后我们只需要每次带着这个配置文件,然后每次修改PROJECT_NAME,这样就可以直接很方便的使用了

{% note info %}
文件日志通常不选择覆盖写入,而是跟在后面写入,即'a'
{% endnote %}

## 我个人的python工作流

https://github.com/luzhixing12345/python-template