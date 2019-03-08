#! /usr/bin/env python3
#-*- coding:utf-8 -*- 

'''群聊聊天室
  功能:类似qq群功能
    1.有人进入聊天室,需要输入姓名,姓名不能重复
    2.进入聊天室时,其他人会收到通知: xxx 进入了聊天室
    3.一个人发消息,其他人会收到: xxx:xxxxxxxxxxx
    4.有人退出聊天室,则其他人也会收到通知: xxx 退出了聊天室
    5.扩展功能:服务器可以向所有用户发送公告:管理员消息: xxxxxxx
'''
#udp client

import socket,os,sys
#服务器的网络地址
ADDR = ('127.0.0.1',9553)

#给server发消息
def send_msg(s,name):
    while True:
        try:
            text = input('please talk:')
        #无论发生什么异常,都退出
        except KeyboardInterrupt:
            text = 'quit'
        #去除左右两边的空字符
        if text.strip() == 'quit':
            msg = 'Q ' + name
            s.sendto(msg.encode(),ADDR)
            #退出进程
            sys.exit('you already exit chatroom')
        #自己定制协议规则 C +text为聊天消息
        msg = 'C %s %s' % (name,text)
        s.sendto(msg.encode(),ADDR)

#收server的消息
def recv_msg(s):
    while True:
        data,addr = s.recvfrom(2048)
        #如果服务器发送退出信息
        if data.decode() == 'EXIT':
            sys.exit('exit parent')
        #打印接收到的聊天消息
        print(data.decode()+'\nplese talk:',end='')

#创建网络连接
def main():
    #创建udp套接字
    sockfd = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    
    while True:
        name = input('please input name:')
        #自己定制协议规则,L +name 格式的字符串为发送的姓名信息 和get类似
        msg = 'L '+ name 
        #发送请求给server
        sockfd.sendto(msg.encode(),ADDR)
        #等待回应
        data,addr = sockfd.recvfrom(1024)
        #允许登录
        if data.decode() == 'OK':
            print('register success.已进入聊天室')
            break 
        #不允许登录
        else:
            print(data.decode())
    #创建新的进程
    pid = os.fork()
    if pid < 0:
        sys.exit('error!')
    #子进程发送消息
    elif pid == 0:
        #连名字一起告诉服务器
        send_msg(sockfd,name)
    #父进程接收消息
    else:
        recv_msg(sockfd)


if __name__ == '__main__':
    main()


