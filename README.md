# CMCC-PTU-Reconnector
 如果使用路由器来连接莆田学院的CMCC-PTU实现宿舍网，会经常掉线需要重新登录，这项目能在不占用任何前台操作资源的前提下完成自动重新登录
 
基本原理：通过往在线网站频繁发送请求以判断当前网络是否有效，如果无效就通过requests抓取验证码并且用ddddocr识别验证码 并且提交账号+密码+验证码以实现重新连接

要求python版本<=3.9 并且连上宿舍wifi（不需要联网）

用法：进入项目cmd输入

```
	  pip install -r requirements.txt
```

安装项目依赖包
```
	  python start.py
```
 运行项目输入账号密码即可
