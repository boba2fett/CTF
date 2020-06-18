#!/usr/bin/env python3
import sys, os
from Crypto.PublicKey import RSA
import binascii, base64
import sympy
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Random import new as Random
from base64 import b64encode
from base64 import b64decode
from Crypto.Util.number import long_to_bytes

# read the public key in:
pubkey = RSA.importKey(open('pubkey.pem', 'r').read())
n=pubkey.n
e=pubkey.e
print(n,e)

ct=int(open('message.txt', 'r').read())
print(ct)


for d in range(0, 2**0xff):
    pt = pow(ct, d, n)
    if b"CSCG{" in long_to_bytes(pt):
        print(long_to_bytes(pt))
        break




exit()
p=0
for i in sympy.primerange(2, 1000000000):
    if n%i==0:
        print(i)
        p=i
        break
print(n%p)
q=n//p


#exit()
def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
        gcd = b
    return gcd, x, y

ct=int(open('message.txt', 'r').read())

#n = p*q #product of primes
phi = (p-1)*(q-1) #modular multiplicative inverse
gcd, a, b = egcd(e, phi) #calling extended euclidean algorithm
d = a #a is decryption key
if d<0:
    d+=phi

pt = pow(ct, d, n)
print(long_to_bytes(pt))

exit()

print("d_hex: " + str(out))
print("n_dec: " + str(d))

pt = pow(ct, d, n)
print("pt_dec: " + str(pt))

out = hex(pt)
out = str(out[2:-1])
print("flag")
print(out.decode("hex"))