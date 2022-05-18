# aipao-runner

爱跑科技阳光体育服务平台Python自动跑步脚本
本项目可以实现自动跑步并将结果发送到邮箱，要使用此项目请更改文件中的以下参数：
```python
msg_from = 'sender@example.com'  #发送方邮箱
smtp = 'smtp.example.com'  #发送方smtp服务器
passwd = 'password_of_sender@example.com'  #发送方邮箱密码
msg_to = 'recv@example.com'  #收件方邮箱
IMEI = 'change_with_your_imei'  #你的imei
```
## 关于IMEI

IMEI即国际移动设备识别码（International Mobile Equipment Identity，IMEI），即通常所说的手机序列号、手机“串号”，用于在移动电话网络中识别每一部独立的手机等移动通信设备，相当于移动电话的身份证。

阳光体育app使用IMEI来识别每个学生的设备，但是由于安卓10以上的系统禁止了非系统应用获取手机IMEI的权限，默认将在学生使用微信登陆时生成一个假的IMEI作为识别码使用，所有会出现“IMEI过期”这种情况出现。

## 如何获取IMEI

可以通过电脑开启Fiddler的http代理然后手机连接代理抓包的方法获取IMEI，缺点是手机要和电脑处于同一网段下并且路由器关闭AP隔离，具体方法请自行探索。