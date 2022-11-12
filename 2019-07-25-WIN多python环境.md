---
layout: post
title: win10多python环境切换
date: 2019-7-25 22:00
comments: true
categories: 技术
---

![](https://upload.wikimedia.org/wikipedia/en/c/cd/Anaconda_Logo.png)


现在基本是python3走天下了，但偶尔有些例外，比如当前需要的esp32开发环境。其实乐鑫提供的[工具](https://docs.espressif.com/projects/esp-idf/zh_CN/latest/get-started/windows-setup.html)可以直接安装python2.7，但最好不要这么用，会造成环境的混乱，比如我的python3+pyqt环境可能就会出现问题。正确的方式是利用conda来管理所有的python版本。

### 1. 新建py27环境
打开anaconda，点击新建环境后选中python版本2.7，然后名字就叫py27。等待片刻，anaconda就帮忙建好了新的环境，接下来就是在命令行的操作。

在cmder命令行中，输入命令：

    conda info -e
    
会显示当前conda管理的环境列表，我的如下：

    base                  *  d:\Anaconda3
    mk                       d:\Anaconda3\envs\mk
    py27                     d:\Anaconda3\envs\py27

表示本地有3个环境，当前使用的是base，其中py27是刚建立的python2.7环境。

### 2. 使用py27环境
conda提供了切换的脚本供我们在环境间切换，其命令是

    activate py27
    
active其实指向的是active.bat，可怜的是这个脚本只能在cmd下才生效，在powershell(也即cmder)环境下并不可用！  为了在cmder中使用active命令，需要安装如下：（参考的[这里](http://yuhao.me/zai-powershellzhong-shi-yong-condade-activate.html)）：

    conda install -n root -c pscondaenvs pscondaenvs

这样会安装与环境切换相关的三个命令：``` activate.ps1 ```, ```deactivate.ps1```, ``` invoke_cmdscript.ps1 ```; 再次使用命令切换，并显示python版本，即可验证正常：

    activate py27
    python -V

现在上面的这个activate指向了activate.ps1，所以正常；

这样，在需要esp32开发时候手动切换到py27环境即可，甚至可以开多个窗口，使用不同的python版本，非常方便。


