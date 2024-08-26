import subprocess as sp
output = sp.getoutput('ssh root@10.227.14.177 ls /tmp')
print (output)
