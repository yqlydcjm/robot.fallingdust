#robot.fallingdust
_____
##qq机器人  
本项目使用go-cqhttp，使用步骤  
## 步骤一
在目录终端输入requirements.txt回车
## 步骤二
在config.yml中写下自己的qq账号和密码（注意：容易被封号建议用小号）  
## 步骤三
本项目内接chatgpt需要在chatgpt.py中写下你的chatgpt的密钥  
然后提问格式为"提问 xxx"  
而且可以绑定某个人发言时回复固定内容只需把那个人的qq号和要回答的文字写在数据库database.sqlite即可  
内置有群发功能只需在main.py中把账号写上你另一个账号的qq号  
在群中发送历史上的今天可以返回历史上的今天都有什么事发生  
发送"捣 qq账号"即可返回这个人头像的表情包  
输入"bmi 体重身高"即可返回你的bmi值并且返回你胖不胖  
如果你想被人发送某段话就返回相应的文字可以在main.py的80-95处添加相应代码照葫芦画瓢  


