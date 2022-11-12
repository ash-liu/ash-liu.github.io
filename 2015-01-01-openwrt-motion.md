--- 
layout: post
date: 2015-07-17  
title: openwrt玩转摄像头——动作检测功能
--- 

前面在网页显示里面用到了mjpg-streamer，这个工具单独拿来显示视频流是很不错的，但是和我们想达到的目标太过遥远，所以我们继续玩转更强悍的工具：**motion**。现在才应该算是真正的开始，之前的那个仅仅是测试下摄像头。

### 关于motion

motion的官方网址在[这里](http://www.lavrsen.dk/foswiki/bin/view/Motion/WebHome)，总的来说motion是一个可以从摄像头检测出画面变化的工具，在画面变化时(比如有人闯入，或者光线异常等)motion会保存画面，或者保存mpeg(通过ffmpeg)，还可以通过配置在这些事件发生时触发外部的命令，比如发送异常提醒邮件，sms等等。同时它也可以提供http流的实时观看。。真是强大的工具，基本上已经实现了我们所需的核心功能。

### 添加motion

进入到openwrt的配置里面，可以发现已经包含了motion，直接勾选后编译下载。进入系统后，会发现/etc/motion.conf，为了方便修改，我们把它复制到自己的目录，然后编辑：

	cp /etc/motion.conf /root/
	cd /root
	vi motion.conf

里面是各种功能配置，每一个参数都可以看看，里面的注释非常的详尽。初次运行，我们大概需要关心一下的参数：  

1. daemon，是否以后台运行，为了方便我们看log以及随时修改，建议关掉；
2. videodevice，我们当然是/dev/video0;
3. width,height,framerate,长宽和帧率。最大可以设置到640*480，帧率设置10左右足以；
4. stream_localhost,这个选on的话，就无法在其他机器上通过http查看，设置为off才可以，所以我们off；
5. target_dir,图片已经视频的存储目录，我们暂时设置个/root，后期会设置到U盘里面。
6. threshold,检测的灵敏度，数值越大越不灵敏。
7. 其他默认；

在/root下面运行

	motion -c motion.conf

启动motion，不出意外的话，会提示错误，显示打开/dev/video0错误。这是因为我们开启了mjpg-streamer，它会开机启动并占用掉我们的cideo0设备，所以首先关掉这个：

	/etc/init.d/mjpg-streamer stop

再次运行就一切正常了。我们可以在摄像头前面晃动物体，motion就会提示检测到异动，并保存图片，也可以通过web访问openwrt的8081端口，和mjpg-streamer一样的效果，通过http查看到实时的画面。

### 存在的问题

目前，我们至少存在2个问题：

1. 图片的存储空间不足。flash可用的也就那么几M，所以得外挂存储空间；
2. 现有的motion不支持ffmpeg。上面并没有提到添加ffmpeg，因为就算添加了还是一样的效果，都会提示ffmpeg的配置参数无效。所以得添加motion对ffmpeg的支持；
3. 由于ffmpeg有4M以上的体量，所以需要安装ipkg到外挂存储空间；

### 外挂存储空间

这个最方便的解决办法当然是使用U盘了，但是rt5350只有一个u口，为了同时接U盘和摄像头，还需要外挂一个USB hub，刚好我手头有一个杂牌hub，接上即可工作。这里有2点需要注意：

1. 供电power，如果是使用5V1A的电源，在拔插usb的时候可能会电压异常，从而导致系统重启，一个U盘，一个摄像头，还有个hub，确实比较吃电。最好的办法是直接换成5V3A的，妥妥的稳定了。
2. 偶尔在拔掉USB hub时候会有kernel module提示错误，一长串的调用栈打印信息。由于不影响使用，我就懒得管它了。

U盘的挂载，可以参考我之前的[文章](http://scriptogr.am/ashliu/post/owusb)，

### 添加motion对ffmpeg的支持

其实一直在说ffmpeg，应该是不准确的，应该是libffmpeg才对，真正的ffmpeg只是一个命令行工具，libffmpeg才是我们真正需要的。

这个问题我前后花了不少时间，因为是一直在研究motion的官方文档，所以进展很慢，还有个原因就是不能上googe...我的vpn在家用没问题，一到公司就不行，感觉应该是dns的问题，但是设置了就是不对，奇葩。后来还是借助于ggncr才找到了[这里](https://forum.openwrt.org/viewtopic.php?id=56786)，参考zloop的Makefile即可实现对ffmpeg的支持。

直接替换掉package/feeds/packages/motion/Makefile，然后进入make menuconfig就可以勾选带ffmpeg的motion了。打开Makefile查看下内容，其实变化并不大，仅仅添加了一些编译选项，可见source code原本就支持的。

编译没有错误，但是会发现没有生成sysupgrade.bin，原因前面已经提到了，那就是libffmpeg太大，最终会使bin档超过8M的限制，所以LZMA就不会生成它。我们可以先不勾选motion-ffmpeg和libffmpeg，生成一个小的系统，先下载进去，然后再勾选motion-ffmpeg后make一次，虽然不会生成最终的sysupgrade.bin，但是可以在bin/ramips/packages/packages/下面找到单独的libffmpeg和motion-ffmpeg安装文件，我们通过U盘单独安装它们即可。

### 添加libffmpeg

openwrt使用opkg来管理包系统，在联网的情况下，可以直接通过opkg来在线安装一些工具，非常的方便。我们这里则是使用opkg来安装本地文件。

把motion-ffmpeg和libffmpeg的包复制到U盘，然后插入开发板。我们首先需要让opkg添加一个到U盘的安装目标，编辑/etc/opkg.conf，在里面添加一个dest

	dest usb /mnt/sda4

然后进入U盘，先执行libffmpeg的安装

	opkg install -d usb libffmpeg-full_*.ipk

会出现2个错误：其一是提示在/usr/lib/opkg/info/下面缺少ffmpeg.xxxx文件；其二是提示无法创建一些链接。

进入/usr/lib/opkg/info/可以发现确实没有，但是在U盘下面的./usr/lib/opkg/info/下面会发现所有的文件都在，于是果断全部copy到系统目录下面，再次安装就不会提示这个错误了。这应该算是一个opkg的小bug，-d指定目录后还是失效了。

对于无法创建连接的问题，也应该是-d的bug。进入U盘下面的./usr/lib，发现所有的文件都在，只不过没有创建link，也懒得link了，直接手动改个名字，把版本的后两位安装错误的提示全部去掉即可。

这样，libffmpeg就安装完成了。

motion-ffmpeg由于比较小，可以直接用：

	opkg install motion*.ipk

安装到系统里面去。


安装完成后，还需要设置一些环境变量，让shell能够找到我们在U盘中的位置，编辑/etc/profile，添加

	export LD_LIBRARY_PATH="/mnt/sda4/usr/lib:/mnt/sda4/lib"
	export PATH=/usr/bin:/usr/sbin:/bin:/sbin:/mnt/sda4/usr/bin:/mnt/	sda4/usr/sbin

然后执行：

	source /etc/profile

来更新环境变量。  
至此，motion和ffmpeg就全部就绪。

### 最后的效果

**最后的效果不是很理想**。原因在于开发板性能不足，无法承载过大的压力。别的不谈，但就一个ffmpeg编码640x480就扛不住了，会直接把内存爆掉，不管设置多少帧率都不行。。所以只能用320x240，小的可怜，而且帧率也就十几的样子。

除却性能不谈，功能上面，现在可以达到的功能：

1. 在线视频http的实时查看；
2. 异常检查时候email报警(这个暂时没做，但是问题不大)；
3. 异常时候图片截图；
4. 异常时通过ffmpeg编码视频存储；

**下一个目标是视频在网盘的存储。**

