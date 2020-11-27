from microWebSrv import MicroWebSrv
import camera
import urequests
import ujson,base64,time
import _thread
import gc



with open("config.json",'r') as f:
    conf=ujson.loads(f.read())

camera.init(0, format=camera.JPEG) 
if conf['pixel'] =='1':
    camera.framesize(camera.FRAME_QQVGA)
elif conf['pixel'] =='2':
    camera.framesize(camera.FRAME_240X240)
elif conf['pixel'] =='3':
    camera.framesize(camera.FRAME_QVGA)
elif conf['pixel'] =='4':
    camera.framesize(camera.FRAME_VGA)
elif conf['pixel'] =='5':
    camera.framesize(camera.FRAME_SVGA)
elif conf['pixel']=='6':
    camera.framesize(camera.FRAME_HD)
else:
    camera.framesize(camera.FRAME_240X240)

import network

ap= network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="mc", authmode=network.AUTH_WPA_WPA2_PSK, password=conf['set_password'])

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
try:
    ap_list=sta_if.scan()
except Exception as e:
    ap_list=[]     
se="<select name='wifi' class='form-control'>"
for i in ap_list:
    se=se+"<option value ='%s'>%s</option>" % (bytes.decode(i[0]),bytes.decode(i[0]),)
se=se+"</select>"

if len(conf['password'])>7:
    sta_if.connect(conf['wifi'],conf['password'])




def wjson(wifi,password,set_password,url,keys,action,pixel):
    js={"wifi":wifi,"password":password,"set_password":set_password,"url":url,"keys":keys,"action":action,"pixel":pixel}
    jsstr=ujson.dumps(js)
    print(jsstr)
    with open("config.json",'w') as f:
        f.write(jsstr)

@MicroWebSrv.route('/')
def _index(httpClient, httpResponse) :
	content = """\
	<!DOCTYPE html>
	<html lang=en>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="/b.css">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
        	<meta charset="UTF-8" />
            <title>ESP32-CAM设置</title>
        </head>
        <body class="container">
            <h1>ESP32-CAM设置</h1>
            <br />
			<form action="/" method="post" accept-charset="ISO-8859-1">
				CAM密码: <input type="text" name="set_password" class="form-control" value="12345678"><br />
				WIFI名称: %s <br />
                wifi名称不显示请点击<a href="/in" class="btn btn-sm btn-primary">手动填写</a><br>
                wifi密码: <input type="password" name="password" class="form-control"><br />
				上传文件路径: <input type="text" name="url" class="form-control" ><br />
				key: <input type="text" name="keys" class="form-control" ><br />
				分辨率:<select class="form-control" name="pixel">
                    <option value="1">120x160</option>
                    <option value="2">240x240</option>
                    <option value="3">320x240</option>
                    <option value="4">640x480</option>
                    <option value="5">800x600</option>
                    <option value="6">1280x720</option>
                </select>
                <br/>
                <input type="submit" value="提交修改" class="btn btn-info">
			</form>
        </body>
    </html>
	""" % (se,)
	httpResponse.WriteResponseOk( headers= None,contentType	 = "text/html",contentCharset = "UTF-8",content = content )

@MicroWebSrv.route('/in')
def _index2(httpClient, httpResponse) :
	content = """\
	<!DOCTYPE html>
	<html lang=en>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="/b.css">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
        	<meta charset="UTF-8" />
            <title>ESP32-CAM设置</title>
        </head>
        <body class="container">
            <h1>ESP32-CAM设置</h1>
            <br />
			<form action="/" method="post" accept-charset="ISO-8859-1">
				CAM密码: <input type="text" name="set_password" class="form-control" value="12345678"><br />
				WIFI名称: <input type="text" name="wifi" class="form-control" value="12345678"><br />
                wifi名称不显示请点击<a href="/" class="btn btn-sm btn-primary">自动填写</a><br>
                wifi密码: <input type="password" name="password" class="form-control"><br />
				上传文件路径: <input type="text" name="url" class="form-control" ><br />
				key: <input type="text" name="keys" class="form-control" ><br />
				分辨率:<select class="form-control" name="pixel">
                    <option value="1">120x160</option>
                    <option value="2">240x240</option>
                    <option value="3">320x240</option>
                    <option value="4">640x480</option>
                    <option value="5">800x600</option>
                    <option value="6">1280x720</option>
                </select>
                <br/>
				<input type="submit" value="提交修改" class="btn btn-info">
			</form>
        </body>
    </html>
	""" 
	httpResponse.WriteResponseOk( headers= None,contentType	 = "text/html",contentCharset = "UTF-8",content = content )


@MicroWebSrv.route('/', 'POST')
def _post(httpClient, httpResponse) :
    formData  = httpClient.ReadRequestPostedFormData()
    wifi = formData["wifi"]
    password  = formData["password"]
    set_password  = formData["set_password"]
    url  = formData["url"]
    keys  = formData["keys"]
    # action  = formData["action"]
    action  = '1'
    pixel = formData["pixel"]

    wjson(wifi,password,set_password,url,keys,action,pixel)
    content = """\
	<!DOCTYPE html>
	<html lang=en>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="/b.css">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
        	<meta charset="UTF-8" />
            <title>ACFUN Clock设置</title>
        </head>
        <body class="container">
            <div class="jumbotron">
            <h1>ESP32监控</h1>
            <p>已经完成配置，请重新断开电源。</p>
            </div>
        </body>
        </html>
    """
    httpResponse.WriteResponseOk(headers=None,contentType="text/html",contentCharset="UTF-8",content=content)
@MicroWebSrv.route('/img')
def _img(httpClient, httpResponse) :
    x=camera.capture()
    content=base64.b64encode(x)
    httpResponse.WriteResponseOk( headers= None,contentType	 = "text/html",contentCharset = "UTF-8",content = content )
@MicroWebSrv.route('/live')
def _live(httpClient, httpResponse) :
    content="""
    <!DOCTYPE html>
	<html lang=en>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="/b.css">
            <script src="/jquery.js"></script>
            <script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
        	<meta charset="UTF-8" />
            <title>ESP32-CAM</title>
        </head>
        <body class="container">
                <div class="row">
                    <div class="col-md-6 col-md-offset-3">
                        <h3>
                            LIVE 直播
                        </h3>
                    </div>
                    <div class="col-md-6 col-md-offset-3">
                        <img width="100%">
                    </div>
                </div>
                <script>
                    function live(){
                        $.ajax({
                            url:"img",
                            success:function(data){
                                $("img").attr("src","data:image/jpg;base64,"+data)
                            }
                        })
                    }
                    setInterval(live,400)
                </script>         
        </body>
        </html>


    """
    httpResponse.WriteResponseOk( headers= None,contentType	 = "text/html",contentCharset = "UTF-8",content = content )


def upload(img,conf):
    form={}
    form['keys']=conf['keys']
    form['img']=base64.b64encode(img)
    print('uploading image')
    a=time.time()
    try:
        urequests.post(conf['url'],data=ujson.dumps(form))
    except Exception as e:
        print(e)
    print(time.time()-a)
    del form
    gc.collect()
    
def oac(abc):
    q=0
    while 1:
        x=camera.capture()
        upload(x,conf)


if sta_if.isconnected() and len(conf["url"])>10:
    _thread.start_new_thread(oac,(conf,))

srv=MicroWebSrv(webPath=".")
srv.Start()
