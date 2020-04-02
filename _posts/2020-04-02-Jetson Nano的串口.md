---
layout: post
title: Jetson Nano的串口
date: 2002-4-2 14:00
comments: true
categories: 技术
---

![](http://ashliu.com/pic/20200402.jpg)

昨天看jetson nano的文档，还发现了一个好玩的点：**它的micro usb口居然是直接支持串口的！**

网上有很多讲怎么设置jetson nano的串口，都是采用的J44接口，该接口里面有3个pin，是TTL电平的串口，可以直接作为tty终端使用。当然了，使用也是非常麻烦，使用条线不说，还需要ttl转sub的dangle，会导致携带使用不方便。

昨天再次看jetson nano的文档，发现了一段描述：原来mirco usb除了可以供电，还可以在使用DC Power的情况下，作为串口终端使用。使用方法也比较简单：

1. 使用跳线帽短接J48，目的是选择外部DC Power供电；
2. 插入5V/2A的DC Power；
3. 使用usb线连接jetson nano的mirco usb与电脑；
4. 在设备管理器中查看COM端口号(WIN10是默认就驱动好了串口，如果没有驱动则需要寻找安装驱动)；
5. 使用putty等终端工具连接；

有了这个就比较方便调试了，因为不管是wifi还是网络接口，都不是很方便得到ip。甚至如果是wifi的话，连接wifi输入密码也是个难题。有了终端，这些都比较容易解决。
