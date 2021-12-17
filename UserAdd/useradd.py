import sys, os, crypt, datetime

if len(sys.argv) == 3:
	uname = sys.argv[1]
	passwd = sys.argv[2]
	comment = ''
elif len(sys.argv) == 4:
	uname = sys.argv[1]
	passwd = sys.argv[2]
	comment = sys.argv[3]
else:
	print('Syntax Error: useradd.py username password [comment]')
	sys.exit(0)

def UserExists():
	df = os.popen("cat /etc/passwd | cut -d ':' -f 1")
	res = df.read()
	res = res.split('\n')
	if uname in res:
		print('Error user exists')
		sys.exit(0)

def maxUid():
	df = os.popen("cat /etc/passwd | cut -d ':' -f 3")
	res = df.read()
	uids = res.split('\n')
	uids = uids[0:len(uids) - 1]
	uids = [int(uid) for uid in uids]
	uids.remove(65534)
	return max(uids)

def createHomeDir():
	df = os.popen('mkdir /home/' + uname + ' ; ' + 'cd /home/' + uname + ' ; ' + 'mkdir Desktop Download Pictures Studies Tools Documents Music Public Templates Videos')
	df.read()
	df = os.popen('cp /etc/skel/.* /home/' + uname)
	df.read()
	df = os.popen('chown -R ' + uname + ':' + uname + ' /home/' + uname)
	df.read()

def updatePasswd(uid):
	f = open('/etc/passwd', 'a')
	f.write(uname + ':x:' + str(uid) + ':' + str(uid) + ':' + comment + ':/home/' + uname + ':/bin/sh\n')
	f.close()

def updateGroup(uid):
	f = open('/etc/group', 'a')
	f.write(uname + ':x:' + str(uid) + ':\n')
	f.close()

def updateShadow():
	hash = crypt.crypt(passwd)
	f = open('/etc/shadow', 'a')
	epoch = (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).days
	f.write(uname + ':' + hash + ':' + str(epoch) + ':0:99999:7:::\n')
	f.close()

def userAdd():
	UserExists()
	uid = maxUid() + 1
	updatePasswd(uid)
	updateGroup(uid)
	updateShadow()
	createHomeDir()

userAdd()
