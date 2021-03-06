--- 
layout: post
date: 2015-07-15  
title: openwrt玩转摄像头——网页显示视频
--- 

### 起因

最近逛众筹网站比较多，发现好多摄像头系列的玩意，刚好我们一个老板他们公司也是做智能摄像头这一块的，所以就动起了玩一玩摄像头的心思。感觉只要不是玩得太深入，都没有太大的难度，拼合组装已有的开源项目就可以实现许多好玩的功能。说玩就玩，初步的目标是实现以下功能：

1. 在线查看摄像头的视频；
2. 保存视频到本地(U盘)；
3. 保存视频到类似百度云等网盘；
4. 入侵检查并email或者短信报警；

其实市面上常见的智能摄像头，也就只有这些功能，由于我的板子没有audio的硬件，就算了。

### 摄像头的选择

市面上的摄像头千千万万，可选的也非常多，为了方便linux的驱动，最好是使用UVC输出的，具体的品类可以参考[这里](http://www.ideasonboard.org/uvc/#devices)，我使用的是微软HD-3000，京东报价100多。到手之后直接连接电脑看了下效果，感觉一般般，稍微比MBA自带的30w像头好那么一点点。

### mjpg-streamer的使用

为了在web上面看到视频，最简单的就是使用mjpg-streamer了。mjpg-streamer是专门用来把jpg转化成mjpeg流输出的工具，它和ffmpeg有点像，有各种的输入输出组件，比如可以选择UVC-camera或者文件等作为输入，选择http或者文件作为流文件的输出。对于我们的需求来说：camera作为输入，经过转化，http作为输出。

真正的使用是很简单的，直接在LuCI-->Applications-->luci-app-mjpg-streamer勾选即可。为了kernel识别我们的摄像头，还需要勾选Kernel modules-->Video Support里面的video core以及下面的各种格式(我们主要用到的是uvc)。我看网友说要勾选Kernel modules-->usb Support下面的kmod-usb-storage-extras，我也直接勾选了，没有验证是否一定需要。

下载固件到开发板，进入web管理页面，在服务下面就可以找到mjpg-streamer，点开启服务。进入8080端口，就会发现视频已经出来了，虽然就一个光秃秃的视频。如果想web页面功能更加丰富，可以把mjpg-streamer source code下面的www文件夹拷贝到ow下面的/www/webcam，或者简单的做法是在menuconfig的时候勾选包含完整的www目录。


