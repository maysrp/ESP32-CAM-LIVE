# ESP32-CAM-LIVE
ESP32-CAM 局域网 直播摄像头  
  
  
你需要一个ESP32-CAM 其次刷好了micropython固件，推荐固件地址：https://github.com/lemariva/micropython-camera-driver  

## 原理

基于bootstrap3 jquery microwebsrv 搭建的在ESP32-cam的一个小型web服务器。  

使用camera拍摄照片然后base64编码通过ajax 直接将文件写入img标签  

运用urequests将base64后的图片数据通过POST传输到你的服务器。  

## 安装


将项目内全部文件（除了REDME.md和post.php外）上传到你的ESP32-cam之中  

打开你的手机 ，搜索热点mc ，连接密码12345678  

后进入浏览器 http://192.168.4.1 进行设置

配置完成后，断电，重新连接  

直播地址 http://192.168.4.1/live   

如果你将你的ESP32-cam连入局域网，可以使用esp32-cam的局域网的IP进行访问，配合 花生壳的蒲公英 可以远程在线监控。

## 远程备份  

在配置界面（ http://192.168.4.1 ）中一个key和上传文件路径中填入地址，就可以把文件直接上传到你的服务器，默认POST方法，服务器接收文件的格式可以参照文件post.php，其中都的key可以用于验证，范例post.php中未使用。  
主要请使用国内服务器或者局域网的方式，否则上传速度会非常缓慢。

## 视频教程

1. https://www.acfun.cn/v/ac20160536  

2. https://www.bilibili.com/video/BV1zz4y1k7Nh  


