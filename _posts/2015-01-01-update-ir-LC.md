---
layout: post
title: 使用Ds18b20上传温度到LeanCloud
date: 2015-07-1 14:30
Tags: technology
---

### 一些观点
最近LeanCloud好像不怎么稳定，知乎和V2EX上面好多人在说LC的坏话，LC的CEO江宏也专门出来做了说明。我觉得如果是企业级大批量客户的话，频繁的当机确实令人无法忍受，这时考虑迁走是应该的；但作为一般的小项目，我是觉得问题不大，而且这样的状况估计也是越来越少，与其花时间来重建后端或者迁移其他平台，还真不如留下。当然了，前提是LC得改进，改进，再改进，稳定，稳定，在稳定。

-----------------------------

### DS18B20硬件连接
温度传感器我使用的是DS18b20，一个像三极管一样的单总线温度传感器，非常好用。由于板子上面的GPIO0-2都被其他功能占用，所以我直接选择了GPIO7作为ds18b20的信号脚，电源和地分别接到3.3V和GND，然后在GPIO7和3.3v之间上拉一个1k以上的电阻，这样就完成了硬件的连接。


### menuconfig的配置
在OW的menuconfig里面已经包含了DS18b20，在:kernel modules -->w1 support -->kmod-w1.在里面勾选上kmod-w1-master-gpio以及kmod-w1-slave-therm，然后退出编译即可。

w1表示单总线(其会实现为一个bus)，master-gpio表示一个gpio式的控制器，slave-therm表示温度传感设备。为什么要这么复杂呢？因为w1总线上面可以挂载多个控制器，每个控制器下面又可以连接多个从设备，所以需要实现为类似的树状结构。


### DTS文件
这样还没有完，配置好之后，仅仅是有了driver，我们还需要到dts文件中去定义device。首先，定位到~ow/target/linux/ramips/dts目录，找到设备相关的描述文件，我的是mpra2.dts和rt5350.dtsi。

首先是pinctl的分配，把uartf组设置为gpio功能，然后添加kmod-w1-master-gpio的设备描述即可：

	gpio-temp {		compatible = "w1-gpio";		gpios = <&gpio0 7 1>;	};

compatible属性是用来匹配of match table的，必须是w1-gpio，gpios是指定io端口，与我们硬件的连接一致即可。


### 温度的查看
编译下载之后，我们就可以进入系统查看到上面添加的东西了：w1在/sys/bus/下面，master-gpio在/sys/devices/w1_bus_master1/下面，以28-开头的就是ds18b20了。w1总线会每隔10s检测一次总线是否有控制器，所以可以上电情况下热拔插更多的传感器(如果硬件可以hot plug的话)，被检测到之后均会列入这个目录下面。进入控制器的目录(28-开头的那个)，里面有个w1_slave文件，直接cat就可以得到slave返回的输出了，形如：

	0b 02 55 00 7f ff 0c 10 60 : crc=60 YES     
	0b 02 55 00 7f ff 0c 10 60 t=32687

32687就表示32.678度，好热。

我使用的开发板在这里碰到了一些麻烦，总是检测不到18b20，后来使用示波器一看波形，再次发现了这个老问题：**udelay存在误差，真实的延迟时间会是给定参数的2倍**，所以需要把所有delay的时间全部除以2才能让18b20正常的工作。这里为了方便，直接在build目录下面修改文件：build_dir/target-mipsel_24kec+dsp_uClibc-0.9.33.2/linux-ramips_rt305x/linux-3.14.25/drivers/w1/w1_io.c里面的w1_delay函数，把传递进来的参数右移一位即可。这么做有一个缺点，那就是build_dir是一个中间文件，如果某天重新编译的话，这个修改是不起作用的，最好的办法是在package里面添加patch文件，这里我就懒得整了。


### LeanCloud设置
LeanCloud端需要设置的很少，为了方便和安全，专门建立一个HomeT的项目，然后在里面建立了一个T class，T暂时只设置一个类型为string的属性。最后记住app id和app key就算完成了LeanCloud端的设置。


### 编译curl
与LeanCloud通信的方式很多，最适合openwrt使用的肯定是restful api——因为可以直接使用curl工具。进入ow的menuconfig，在network-->file transfer-->curl可以找到(我反反复复找了好久都没有找到，最后没辙了，查makefile文件才找到它..)，然后进入lib-->libcurl-->*里面全部enable，然后再ssh里面勾选openssl。然后退出编译。这里有一点是为什么要带ssl？原因是LeanCloud的restful服务器全部是https的，所以必须得带这个。


### 使用curl
curl的使用可以参考LeanCloud的文档，特别是在线api测试的那个，直接copy过来就可以了。但是这里会出现一个问题：在mac上面是可以成功的，在ow上面却不行，会提示certificate verify failed之类的信息，意思是证书验证失败，可以参考[这里](http://jqlblue.github.io/2014/05/14/a-trouble-in-request-https-in-curl/)，简单的解决办法是使用**-k**参数来取消ssl证书的验证，另一个更新证书的方式我尝试了一下，没有成功。


### lua粘合
最后，使用lua语言简单粘合起来(file:updateT.lua)

	#!/usr/bin/lua

	local util = require("luci.util")

	APP_ID  = ""
	APP_KEY = ""

	function read_T()
		local ret = util.exec("cat /sys/devices/w1_bus_master1/28-0414517510ff/w1_slave")
		return string.sub(ret, -6, -2);
	end

	cmd = "curl -k -X POST -H \"X-AVOSCloud-Application-Id: %s\" -H \"X-AVOSCloud-Application-Key: %s\" -H \"Content-Type: application/json\" -d '{\"t\":\"%s\"}' https://api.leancloud.cn/1.1/classes/T";
	cmd = string.format(cmd, APP_ID, APP_KEY, read_T());
	util.exec(cmd);

添加+x属性，然后把文件丢到/usr/sbin下面。


### cron周期执行
执行crontab -e，在里面加入：

	* * * * *  /usr/sbin/updateT.lua

表示每天的每分钟都执行一次。





