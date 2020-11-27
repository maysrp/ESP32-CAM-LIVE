# ESP32-CAM-LIVE
ESP32-CAM 局域网 直播摄像头  

基于bootstrap3 jquery microwebsrv 搭建的在ESP32-cam的一个小型web服务器。  

使用camera拍摄照片然后base64编码通过ajax 直接将文件写入img标签  

运用urequests将base64后的图片数据通过POST传输到你的服务器。  

将项目内全部文件上传到你的ESP32之中，打开你的手机 ，搜索热点mc ，连接密码12345678，后进入浏览器 http://192.168.4.1 进行设置

直播地址 http://192.168.4.1/live 如果你将你的ESP32-cam连入局域网，可以使用esp32-cam的局域网的IP进行访问，配合 花生壳的蒲公英 可以远程在线监控。
