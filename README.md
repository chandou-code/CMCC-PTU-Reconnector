# CMCC-PTU-Reconnector

## 项目简介

该项目旨在解决使用路由器连接莆田学院CMCC-PTU网络时经常掉线需要重新登录的问题。它可以在不占用任何前台操作资源的前提下，实现自动重新登录。

## 基本原理

通过频繁向在线网站发送请求，判断当前网络是否有效。如果无效，则使用requests库抓取验证码，并通过ddddocr识别验证码。最后提交账号、密码和验证码，实现重新连接。

## 功能特点

- 仅在连接到宿舍WiFi（CMCC-JKL改成自己宿舍的WIFI名字）后才开始检测网络状态，避免无谓的检测。
- 使用随机频率进行断网检测，同时通过一系列不相关的IP来检测网络断连，以提高准确性。
- 即使某些IP被ban，也能通过其他IP继续检测网络状态。

## 使用方法

1. 进入项目目录，打开命令行窗口。
2. 使用以下命令安装项目依赖包：

# 安装项目依赖包
```
pip install -r requirements.txt
```

# 运行项目
```
python start.py
```

# 输入校园网账号和密码即可开始自动重新连接。

## 注意事项

- 要求Python版本不超过3.9。
- 确保已连接到宿舍WiFi，无需联网即可运行。

欢迎使用并提出改进建议！
