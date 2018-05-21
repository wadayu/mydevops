#coding:utf-8
__author__ = 'WangDy'
__date__ = '2018/3/19 13:16'

import pexpect

class PasswdLogin(object):

    def __init__(self,user,password,port,host):
        self.user = user
        self.password = password
        self.port = port
        self.host = host

    def login(self):
        ssh_k = pexpect.spawn('ssh -p %s -l %s %s' %(self.port,self.user,self.host))
        res = ssh_k.expect(['password','continue connecting (yes/no)?'],timeout=5)

        if res == 0:
            ssh_k.sendline(self.password)
        elif res == 1:
            ssh_k.sendline('yes\n')
            ssh_k.expect('password')
            ssh_k.sendline(self.password)

        index = ssh_k.expect(['#',pexpect.TIMEOUT,pexpect.EOF],timeout=5)

        if index == 0:
            print 'Login in as root'
            ssh_k.interact()   #接管子程序，使用终端进行会话。
        elif index == 1:
            print 'process timeout'
        elif index == 2:
            print 'process exit'

if __name__ == '__main__':
    pl = PasswdLogin('root','666666','22','192.168.19.131')
    pl.login()


