f=open("laa2","r")
s=''
for l in f.readlines():
    l=l.strip()
    s=s+'0x'+l+','
print(s)