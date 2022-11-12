--- 
layout: post
date: 2015-07-03 14:00  
title: ow添加Transmission  
--- 

添加Transmission是比较简单的，直接在network-->bittorrent下面，勾选上Transmission的deamon和web选项即可，这里有一点是deamon下面的那个字符串客户端transmission-cli会占用700+K的空间，如果没有必要可以不要，仅仅使用web的就可以了。

编译是没问题的，但是使用起来却有很多障碍: 

1. 首先碰到的是下载一旦超过2M就会让transmission挂掉。使用logreader查看可以发现是内存溢出了，然后进入transmission的配置文件，看到了一个cache大小的配置，其默认为2M，修改为1M，即每缓冲1M就写入磁盘一次。
2. 表现依然是下载不动，进入log查看发现：“**UDP Failed to set receive buffer: requested 4194304, got 327680**”等信息。我记得之前用树莓派的时候，Transmission也出现过同样的错误，google了一通，找到了解决办法，在/etc/sysctl.conf中添加如下配置：

		net.core.rmem_max=4194304     
		net.core.wmem_max=1048576

再次重启transmission服务即可。然并卵，我并不准备在真正的ow上面使用bt，原因是**内存太小了**，拖慢运行速度不说，每1M写一次U盘那真是作死的节奏，想想还是算了，用树莓派那种大内存的玩玩bt还勉强接受，ow这种真的不推荐。

PS，好像忘记说配置文件的事情了，这个google一下多的很。另外，最近资料查的多，不能直接google真实烦人，baidu那货实在是用不了，根本搞不懂我要查的神马。