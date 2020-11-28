<?php
  $post=file_get_contents("php://input");
	$pg=json_decode($post,true);
	$jpg_ob=base64_decode($pg['img']);
	file_put_contents((string)time().".jpg",$jpg_ob);
  #PHP 接受文件的例子，将post文件接受 并且按照时间戳保存在该脚本目录
