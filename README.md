# El-Gamal and RSA Schemes implemented with-Socket-Programming
This program contains socket programming where communication between client and server is end-to-end encrypted by 
+ 1. El-Gamal public-key encryption scheme
+ 2. RSA public-key encryption scheme

File el_gamal.py contains functions required for El-Gamal encryption scheme : get_primitive_root,key generation, encryption, decryption and some auxiliary functions to used in formatting input and output to encryption/decryption functions.

File rsa.py contains functions required for RSA encryption scheme : key generation, encryption, decryption and some auxiliary functions to used in formatting input and output to encryption/decryption functions.

client.ipynb and server.ipynb contain client side and server side code respectively. 
To choose encryption scheme for communication, remove comment in import section for that correspending file (el_gamal.py or rsa.py)

File 'El-Gamal Crypto-scheme.ipynb' is for demonstrating how El-Gamal works.
File 'RSA.ipynb' is for demonstrating how RSA works.

Prime number of 84 bits (25 digits) is used.

Download pyecm.py from https://github.com/martingkelly/pyecm which was used for finding prime factors of large numbers in a very less time.
