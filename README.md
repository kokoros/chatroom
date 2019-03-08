Pro_web:charroom
===================

Getting Started
--------------

* 进入目录: 
     cd chatroom
* 开启服务端:
     python3 chat_server.py

Prerequisites(先决条件)
----------------------
* python3
* pip3 socket 

Running the tests
-----------------
* 开启服务端后再开启客户端:
  python3 chat_client.py
* 可以开启多个客户端

Function
------------------
群聊聊天室  
>>功能:类似qq群功能  
1.有人进入聊天室,需要输入姓名,姓名不能重复  
    2.进入聊天室时,其他人会收到通知: xxx 进入了聊天室  
    3.一个人发消息,其他人会收到: xxx:xxxxxxxxxxx  
    4.有人退出聊天室,则其他人也会收到通知: xxx 退出了聊天室  
    5.扩展功能:服务器可以向所有用户发送公告:管理员消息: xxxxxxx  

Built With
------
* python3
* socket

Authors
-----------
Koro
