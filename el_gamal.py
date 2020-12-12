import numpy as np
import gmpy2
from gmpy2 import powmod,mpz,isqrt,invert
import pyecm

def get_primitive_root(prime):
    # calculate phi(n)
    # phi(prime) is (prime-1)
    phi = prime-1
    prime_factors = list(pyecm.factors(phi, False, True, 10, 1))
    # set range for primitive root
    # so that we don't have to calculate all the roots
    d_range = np.random.randint(20,30)
    possible_root = 5
    while possible_root < prime:
        temp = []
        is_root = True
        for i in range(len(prime_factors)):
            remainder = gmpy2.powmod(possible_root,(phi//prime_factors[i]),prime)
            # if remainder is 1, then current number we're checking is not a primitive root
            if remainder == 1:
                is_root = False
                break
        if is_root and possible_root >= d_range:
            return possible_root
        possible_root=possible_root+1

def generate_keys():
    # prime number of 25 digits i.e 84 bits
    n = 1000000000000000000000000
    random_add = np.random.randint(1,1000000)
    n = n + random_add
    p = int(gmpy2.next_prime(n))
    d = 0
    for i in range(2,p-1):
        select1 = np.random.randint(0,20)
        select2 = np.random.randint(0,20)
        if select1 == select2:
            d=i
            break
    d = mpz(d)
    e1 = get_primitive_root(p)
    e2 = gmpy2.powmod(e1,d,p)
    return e1,e2,p,d

def encrypt(plain_text_blocks,public_keys):
    cipher_text_blocks = []
    e1,e2,p = public_keys
    r = np.random.randint(2,50)
    for plain_text in plain_text_blocks:
        cipher_text1 = gmpy2.powmod(e1,r,p)
        cipher_text2 = ((gmpy2.powmod(e2,r,p))*plain_text)%p
        cipher_text_blocks.append((cipher_text1,cipher_text2))
    return cipher_text_blocks

def decrypt(cipher_text_blocks,secret_key,public_keys):
    e1,e2,p = public_keys
    d = secret_key
    decypted_plain_text_blocks = []
    for cipher_text in cipher_text_blocks:
        cipher_text1,cipher_text2 = cipher_text
        cipher_text1 = gmpy2.powmod(cipher_text1,d,p)
        cipher_text1 = gmpy2.invert(cipher_text1,p)
        cipher_text2 = cipher_text2*cipher_text1
        plain_text = cipher_text2 % p
        decypted_plain_text_blocks.append(plain_text)
    return decypted_plain_text_blocks

# taken in 'Hello World!!!' returns ['Hel','lo ','Wor','ld!','!!']
def get_blocks(PT,block_size):
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
