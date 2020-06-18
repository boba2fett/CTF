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

qta=1067267517149537754067764973523953846272152062302519819783794287703407438588906504446261381994947724460868747474504670998110717117637385810239484973100105019299532993569
msg=6453808645099481754496697330465

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
        gcd = b
    return gcd, x, y

for p in sympy.primerange(2, 100000):
    for q in sympy.primerange(2, 100000):
        n = p*q
        phi = (p-1)*(q-1)
        gcd, d, b = egcd(e, phi)
        if d<0:
            d+=phi
        if pow(msg, d, N) == qta:
            print("CSCG{DUMMY_FLAG}")
            print(p,q)
            exit()


exit()











exit()
if pow(msg, d, N) == qta:
    print("CSCG{DUMMY_FLAG}")
else:
    print("That was not kind enough!")