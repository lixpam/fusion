#!/usr/bin/python
#coding:utf-8

'''
@author lixpam
@brief  short way to connect remote machine
@usage  python ssh_conn.py [user@]hostname
        if user is missed, it takes first one in HOST_LIST
'''

import os
import sys
import pexpect

# 配置服务器列表
HOST_LIST = {
    "test" :
        {
            "ip"   : "192.168.0.100",
            "port" : 22,
            "account" : [
                ['lixpam', 'lixpam_passwd'],
            ],
        },
}

def _ssh(host):
    _user = None
    if '@' in host:
        _user, host = host.split('@')

    if host not in HOST_LIST:
        raise SyntaxError("host '%s' not exist" % host)

    # 没提供user，使用列表中第一个
    host_info = HOST_LIST[host]
    user_info = None
    if _user is None:
        user_info = HOST_LIST[host]['account'][0]
    else:
        for user_info in (x for x in HOST_LIST[host]['account'] if x[0] == _user): break

    if user_info is None:
        raise SyntaxError("host config not exist")

    # 获取登录shell的窗口大小
    win_rows, win_cols = os.popen("stty size").read().split()
    otp = pexpect.spawn('ssh %s@%s -p%s -o StrictHostKeyChecking=no' % (user_info[0], host_info['ip'], host_info['port']))
    otp.expect('.*assword.*')
    otp.sendline(user_info[1])
    # 设置服务器窗口大小
    otp.setwinsize(int(win_rows), int(win_cols))
    # 进入可交互模式
    otp.interact()

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        raise SyntaxError("usage: python ssh_conn.py [user@]name")
    _ssh(sys.argv[1])
