import numpy as np
import gmpy2
from gmpy2 import powmod,mpz,isqrt,invert
import pyecm

def generate_keys():
    # prime number of 25 digits i.e 84 bits
    temp = 1000000000000000000000000
    random_add1 = np.random.randint(1,1000000)
    random_add2 = np.random.randint(1000000,2000000)
    p = int(gmpy2.next_prime(temp + random_add1))
    q = int(gmpy2.next_prime(temp + random_add2))
    n = p*q
    phi = (p-1)*(q-1)
    e = 2
    while True:
        if gmpy2.gcd(phi,e) != 1:
            e = e + 1
        else :
            break
    d = gmpy2.invert(e,phi)
    return n,e,d

def encrypt(plain_text_blocks,public_keys):
    cipher_text_blocks = []
    n,e = public_keys
    for plain_text in plain_text_blocks:
        cipher_text = (gmpy2.powmod(plain_text,e,n))
        cipher_text_blocks.append(cipher_text)
    return cipher_text_blocks

def decrypt(cipher_text_blocks,secret_key,public_keys):
    n,e = public_keys
    d = secret_key
    decypted_plain_text_blocks = []
    for cipher_text in cipher_text_blocks:
        plain_text = (gmpy2.powmod(cipher_text,d,n))
        decypted_plain_text_blocks.append(plain_text)
    return decypted_plain_text_blocks

# taken in 'Hello World!!!' returns ['Hello World!','!!']
def get_blocks(PT,block_size=12):
    blocks = []
    i = 0
    while i<len(PT):
        temp_str=''
        if i+block_size-1 < len(PT):
            temp_str=temp_str+PT[i:i+block_size]
        else :
            temp_str=temp_str+PT[i::]
        blocks.append(temp_str)
        i=i+block_size
    return blocks
        
# covert plain_text block from characters to the numbers
def format_plain_text(PT):
    plain_text_blocks = []
    for block in PT:
        plain_text = 0
        for i in range(len(block)):
            # for 'd'
            if ord(block[i]) == 100:
                plain_text = plain_text*100 + 28
            # between (101,127)
            elif ord(block[i])>100:
                plain_text = plain_text*100 + (ord(block[i])-100)
            else :
                plain_text = plain_text*100 + (ord(block[i]))
        plain_text_blocks.append(plain_text)
    return plain_text_blocks

# convert numeric decypted_plain_text_blocks into a single plain text of characters
def format_decrypted_plain_text(decypted_plain_text_blocks):
    plain_text_blocks = []
    for dc_pt in decypted_plain_text_blocks:
        plain_text = ''
        temp = dc_pt
        # for 'd' temp = 28
        while temp > 0:
            if temp%100 == 28:
                plain_text = plain_text + 'd'
            elif (temp%100) in range(0,27):
                plain_text = plain_text + chr((temp%100)+100)
            else :
                plain_text = plain_text + chr((temp%100))
            temp = temp//100
        plain_text = plain_text[::-1] 
        plain_text_blocks.append(plain_text)
    final_plain_text = ''
    for plain_text_block in plain_text_blocks:
        final_plain_text = final_plain_text + plain_text_block
    return final_plain_text
