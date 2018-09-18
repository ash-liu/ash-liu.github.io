--- 
layout: post
date: 2015-07-14  
title: 编译openwrt现MD5错误
--- 
![image](http://pic.ashliu.com/md5.png)




编译openwrt一般会出现下载错误，从而导致编译中断，所以当出现这个问题的时候，我第一时间是感觉下载的有问题。于是手动下载了一个放到dl里面，再次执行make，结果还是显示md5验证错误。奇怪了，怎么会下载的文档不对呢？仔细看了make信息，发现它定位url使用的文档名字是**cambozola-latest.tar.gz**，看到名字我就感觉问题应该出在这里了。

一般都习惯用latest来表示最新的，这样不仅方便人，也很方便脚本来获取最新的版本，因为都是同样的名字，无需判断是否最新。但是用在类似openwrt的构建系统里面，我感觉是不合适的，对于不同的package理应对到具体的版本号，这样才能够保证make过程的畅通。而且看看其他package的url定位都是具体的版本号，可见这应该是一个小bug(也或许是这个package没有提供具体版本号的下载，所以如果我们自己也做package的话，就一定得引以为戒。)。

解决办法。首先得到cambozola-latest.tar.gz这个文档，然后使用md5命令获取到md5值。进入./feeds/packages/multimedia/mjpg-streamer下面，修改Makefile中关于cambozola的md5值，然后再次编译即可通过。