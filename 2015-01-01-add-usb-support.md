---
layout: post
title: ow添加usb支持
date: 2015-07-1 21:30
Tags: technology
---

### 配置编译
这个开发板一直没有用过usb，最近想着搞一个下载器玩玩，所以添加个usb玩玩。对于ow而言，添加usb是非常简单的事情，配置配置就OK了，需要关注的几个点为：   

1. 在kernel modules-->usb support下面，usb-core为核心必须选择，为了保险起见把ohci和uchi控制器都勾选上(rt5350应该是ohci)，为了支持U盘，勾选上usb2.0以及usb storage选项；
2. 在kernel modules-->block devices下面，选择scsi-core和scsi-generic，以后可以直接使用移动硬盘；
3. 在kernel modules-->filesyatems下面，选择需要的文件系统，我选择了msdos以及vfat。看了下，里面ntfs，nfs等等主流的文件系统都支持，以后想加直接编译进来就行了； 
4. 在Utilities-->disc下面，勾选fdisk工具，用来检查和设置分区；理应添加mount类工具，但貌似busybox已经提供了，所以就不需要额外勾选了。

这样，从底层驱动到上层的工具都已准备完成，编译下载即可。

### 缺少lib的问题
我在这里时遇到了一个问题：**fdisk依赖的libsmartcols找不到！**，这次是grep了所有目录，真找不到。上网一阵乱搜，没有发现其他人有说类似的问题，但是在openwrt的代码库([这里](https://dev.openwrt.org/changeset/43459))里面找到了libsmartcols本应该在的地方：util-linux。通过查看diff可以发现，这个库之前是没有包含的，但后来添加了进来，所以我下载的git分支可能碰巧没有包含(使用./scripts/feeds update util-linux仍然不行)。解决的办法是用代码库里面的util-linux(包含makefile以及patch文件)直接替代我本地的package，然后再次执行make menuconfig就可以在Libraries找到这个库了，勾选或者再次去勾选下fdisk，这个库就会被fdisk强制selected的。

### config异常的问题
本来这样子开开心心的编译一下就搞定了，但结果却非常曲折。首先是提示curl缺少libpolarssl库，可这不科学啊！我分明已经勾选了这个库。这时我猜测也应该是修改上层的package导致config文件产生了混乱，所以想通过/去勾选来让config恢复，结果还是然并卵。最后，我想起来好像没有删除过bin文件夹，同时刚刚在网上看到说make clean就是删除bin的，于是鬼使神差的执行了make clean...结果是被坑了！命令一下去，就是长时间的删除，我一看就知道不对，马上终止，已经来不及了。于是专门跑到openwrt官网一看，尼玛make clean是删除所有中间文件啊，那么我在build_dir里改的那些东西全没了！！但是幸运的是经过2个多小时的build，居然重新成功了！看来还真是config混乱导致的。(看来以后还是需要生成patch文件才好)

### 添加必要的nls
编译成功之后，会发现使用mount仍然无法成功，会提示缺少需要的nls支持，这个可以在kernel modules-->Native Language Support勾选上需要的base，cp437，iso8859-1以及utf8。这样就可以成功mount了。在使用mount的时候，为了显示中文，可以添加-o iocharset=uft8。至此就可以正常的挂载显示u盘内容了。

### 自动挂载
在openwrt里面也可以实现自动挂载和卸载，我参考了[这里](http://www.right.com.cn/forum/thread-102640-1-1.html)中freefall12的脚本。简单解释下:  

1. 首先是文件名/etc/hotplug.d/block/30-usbmount。openwrt使用hotplug(源码在procd下面)来管理系统的事件，也包括了我们这里的usb拔插，所以我们要脚本放在etc/hotplug.d/block/下面，以供hotplug调用，30是启动时候的顺序。
2. 文件里面的add和remve分别对应了插拔事件：在插入的时候，在/dev下面找到设备的名称，然后再/mnt下面建立对应的目录，最后挂载上去；拔出的时候则umount掉所有的设备。

这个脚本应该说是够用的，但是说尽善尽美还谈不上，先这样用着再说。