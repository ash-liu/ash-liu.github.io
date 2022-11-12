---
layout: post
title: Amazon FreeRTOS开发环境搭建(Esp32)问题记录
date: 2019-7-29 20:00
comments: true
categories: 技术
---

![](http://pic.ashliu.com/2019072901.png)


前面在WSL里面整好了esp32的开发环境，可惜并不能直接同于amazon freetros的开发，还需要几个小改动。

首先，需要参考amazon的文档，从这里开始：[什么是Amazon FreeRTOS](https://docs.aws.amazon.com/zh_cn/freertos/latest/userguide/what-is-amazon-freertos.html)，介绍了Amazon FreeRTOS的整体构成，功能等等。

编译环境相关的文档从[这里](https://docs.aws.amazon.com/zh_cn/freertos/latest/userguide/freertos-getting-started.html)开始，个人觉得这一部分的文档稍微有点混乱，原因是有的设置是amazon FreeRTOS相关的，有的设置是vendor相关的，容易混淆。而我碰到的几个问题其实文档都有写，但是看的时候死活就是没发现。

### 问题1：gcc报错：-Werror=sizeof-pointer-memaccess

原因就是按照esp32官方的方式安装的xtensa gcc版本太高了所致。按照[文档](https://docs.aws.amazon.com/zh_cn/freertos/latest/userguide/getting_started_espressif.html)的描述，是因为amazon freetros使用的ESP-IDF版本比较低，无法与最新的xtensa gcc兼容所致，需要在[这里](https://docs.espressif.com/projects/esp-idf/en/v3.1.3/get-started-cmake/linux-setup.html)下载低版本的gcc;


### 问题2：各种Component没有包含

因为按照官方教程设置了IDF_PATH的缘故，amazon freertos里面设置了这个环境变量，会冲突。去掉即可：

    unset IDF_PATH

### 问题3：下载无法使用

与前面官方环境类似，把esptool.py改成esptool.exe即可；

