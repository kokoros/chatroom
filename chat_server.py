#! /usr/bin/env python3
#-*- coding:utf-8 -*- 

'''
Chatroom
env:python3.5
exc:socket and fork
'''
'''
群聊聊天室
  功能:类似qq群功能
    1.有人进入聊天室,需要输入姓名,姓名不能重复
    2.进入聊天室时,其他人会收到通知: xxx 进入了聊天室
    3.一个人发消息,其他人会收到: xxx:xxxxxxxxxxx
    4.有人退出聊天室,则其他人也会收到通知: xxx 退出了聊天室
    5.扩展功能:服务器可以向所有用户发送公告:管理员消息: xxxxxxx
'''
#udp server

import socket,os,sys
#用于存储用户{name:addr}
user = {}

#处理登录
def do_login(s,name,addr):
    #判断姓名是否存在,禁止起名为管理员消息
    if (name in user) or name == "管理员消息":
        s.sendto(b'name already exist',addr)
        return 
    else:
        s.sendto(b'OK',addr)
        #通知其他已存在的client
        msg = '\nwelcome %s enter the chatroom' % name 
        for i in user:
            s.sendto(msg.encode(),user[i])
        #在user字典里加入新来的client
        user[name] = addr 
 
def do_chat(s,name,text):
    msg = '\n%s : %s' % (name,text)
    for i in user:
        #不发消息给自己
        if i!= name:
            s.sendto(msg.encode(),user[i])

#处理退出
def do_quit(s,name):
    msg = '\n%s exit the chatroom' % name 
    #给其他client发送消息,给退出的发送特殊消息
    for i in user:
        if i!= name:
            s.sendto(msg.encode(),user[i])
        else:
            s.sendto(b'EXIT',user[i])
    #将用户删除字典
    del user[name]

def do_requests(s):
    while True:
        #接受client 信息
        data,addr = s.recvfrom(1024)
        msgList = data.decode().split(' ')
        #判断第一项是否为'L',是否为姓名信息
        if msgList[0] == 'L':
            do_login(s,msgList[1],addr)
        elif msgList[0] == 'C':
            #重新组织消息内容
            text = ' '.join(msgList[2:])
            do_chat(s,msgList[1],text)
        #如果收到了退出的信息
        elif msgList[0] == 'Q':
            do_quit(s,msgList[1])

#创建网络连接
def main():
    #网络地址
    ADDR = ('0.0.0.0',9553)
    #创建udp套接字
    sockfd = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    #重置端口
    sockfd.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    #绑定网络地址
    sockfd.bind(ADDR)
    #创建单独进程,发送管理员消息
    pid = os.fork()
    if pid < 0:
        print('Error')
        return 
    #子进程 发送管理员消息
    elif pid == 0:
        while True:
            msg = input('管理员message:')
            msg = 'C 管理员消息 ' + msg
            #在子进程中,给服务端自己发送消息,即消息被父进程中的处理各种客户端请求所接受
            sockfd.sendto(msg.encode(),ADDR)
    #父进程
    else:
        #处理各种客户端请求
        do_requests(sockfd)


if __name__ == '__main__':
    #执行网络连接
    main()