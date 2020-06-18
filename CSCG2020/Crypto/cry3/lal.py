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


def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
        gcd = b
    return gcd, x, y

def modinverse(a, n):
    g, u, v=egcd(a, n)
    return u%n

def nth_root(x, n):
    # Start with some reasonable bounds around the nth root.
    upper_bound = 1
    while upper_bound ** n <= x:
        upper_bound *= 2
    lower_bound = upper_bound // 2
    # Keep searching for a better result as long as the bounds make sense.
    while lower_bound < upper_bound:
        mid = (lower_bound + upper_bound) // 2
        mid_nth = mid ** n
        if lower_bound < mid and mid_nth < x:
            lower_bound = mid
        elif upper_bound > mid and mid_nth > x:
            upper_bound = mid
        else:
            # Found perfect nth root.
            return mid
    return mid + 1



# read the public keys in:
pubkey = RSA.importKey(open('german_government.pem', 'r').read())
n1=pubkey.n
e1=pubkey.e



pubkey = RSA.importKey(open('us_government.pem', 'r').read())
n2=pubkey.n
e2=pubkey.e


pubkey = RSA.importKey(open('russian_government.pem', 'r').read())
n3=pubkey.n
e3=pubkey.e

assert(e1==e2==e3),"lol not same"

# read in the cipher texts
l=open('intercepted-messages.txt', 'r').readlines()
ct1=int(l[0].strip().split(": ")[1])
ct2=int(l[1].strip().split(": ")[1])
ct3=int(l[2].strip().split(": ")[1])

#ct=(ct1*ct2*ct3)%(n1*n2*n3)

#print(egcd(n1,n2))
#print(egcd(n1,n3))
#print(egcd(n2,n3))









m=n1*n2*n3
M1=(n2*n3)
M2=(n1*n3)
M3=(n1*n2)

x1=modinverse(M1,n1)
x2=modinverse(M2,n2)
x3=modinverse(M3,n3)

print(x1)
print((M1*x1)%n1==1)
print(x2)
print(x3)

solu=ct1*M1*x1+ct2*M2*x2+ct3*M3*x3
solu=solu%m
print(solu%n1==ct1)
print(solu%n2==ct2)
print(solu%n3==ct3)

r=nth_root(solu, 3)
print(r)
print(long_to_bytes(r))

exit()

cube=cube%m
r=nth_root(cube, 3)
print(r)
print(long_to_bytes(r))

exit()

#n2*n3*x1=m**3%n1
#n1*n3*x2=m**3%n2
#n1*n2*x3=m**3%n3

x,x1,x=egcd(n2*n3,ct1)
x,x,x2=egcd(n1*n3,ct2)
x,x,x3=egcd(n1*n2,ct3)

print(x1)
print(n2*n3*x1%n1==ct1)
print(x2)
print(n1*n3*x2==ct2%n2)
print(x3)
print(n1*n2*x3==ct3%n3)

#r=nth_root(ct, 3)
#print(r)
#print(long_to_bytes(r))
exit()














p=0
for i in sympy.primerange(2, 1000000):
    if n%i==0:
        print(i)
        p=i
        break

q=n//p

print(q)

#msg=int(open('message.txt', 'r').read())






#exit()


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