import math, AES
from pprint import pprint


def leftShift(binary_number: int, n: int) -> int:
    return int((format(binary_number, '0' + str(b) + 'b')[1:] + '0'), 2)


def SUBK(K: hex, b: int) -> list:
    '''Generate the SubKeys -K1 and K2- and return them as a list.'''
    # Determine what Rb is in according to block size b
    if b == 64:
        Rb = ('0' * 59) + '11011'
    elif b == 128:
        Rb = ('0' * 120) + '10000111'
    else:
        print('Unvalid block size!')
        exit()
    
    Rb = int(Rb, 2)
    
    # L = AES-128 Encrypted 0^b
    L = AES.encryptAES(message=('0' * 64), key=K, number_of_rounds=10)
    print('CIPHK(0128) =', L)
    L = int(L, 16) # Convert to int to perform shift operations
    
    # Calculate the K1 value
    K1 = leftShift(L, 1) if format(L, '0' + str(b) + 'b')[0] == '0' else leftShift(L, 1) ^ Rb
    print('K1 =', hex(K1)[2:].upper()) # Debug
    
    # Calculate the K2 value
    K2 = leftShift(K1, 1) if format(K1, '0' + str(b) + 'b')[0] == '0' else leftShift(K1, 1) ^ Rb
    print('K2 =', hex(K2)[2:].upper()) # Debug
    
    return (K1, K2)


def CMAC(K, M: hex, K1, K2, b):
    '''Calculate the CMAC value of a given message with SubKeys'''
    # Check if the message is empty string and convert it to binary
    if M != '':
        M = format(int(M.replace(' ', ''), 16), '0' + str(len(M.replace(' ', '')) * 4) + 'b')
    
    Mlen = len(M)
    
    # Calculate the length of 
    n = 1 if Mlen == 0 else math.ceil(len(M) / b)

    Mlist = list()
    for i in range(1, n+1):
        Mlist.append(M[:b])
        M = M[b:]
    
    Mlist[-1] = format(K1 ^ int(Mlist[-1], 2), '0' + str(b) + 'b') if len(Mlist[-1]) == b else format(K2 ^ int(Mlist[-1] + ('1' + ('0' * (n * b - Mlen - 1))), 2), '0' + str(b) + 'b')
    
    C0 = '0' * b
    C = list()
    C.append(C0)
    for i in range(0, n):
        Ci = AES.encryptAES(message=AES.convertToHex(int(C[i], 2) ^ int(Mlist[i], 2), b // 4), key=K, number_of_rounds=10)
        C.append(format(int(Ci, 16), '0' + str(b) + 'b'))
    
    return [AES.convertToHex(int(C[n], 2), b // 4), C]


def AES_CMAC(M, K):
    b = 128
    (K1, K2) = SUBK(K, b)
    (T, C) = CMAC(K, M, K1, K2, b)
    return [T, C]

if __name__ == '__main__':
    K = '2b7e1516 28aed2a6 abf71588 09cf4f3c'
    b = 128
    
    print('EXAMPLE 1: Mlen 0')
    M = ''
    (T, C) = AES_CMAC(M, K)
    print('T =', T, end='\n\n')
    
    print('EXAMPLE 2: Mlen 128')
    M = '6bc1bee2 2e409f96 e93d7e11 7393172a'
    (T, C) = AES_CMAC(M, K)
    print('T =', T, end='\n\n')
    
    print('EXAMPLE 3: Mlen 320')
    M = '6bc1bee2 2e409f96 e93d7e11 7393172a ae2d8a57 1e03ac9c 9eb76fac 45af8e51 30c81c46 a35ce411'
    (T, C) = AES_CMAC(M, K)
    print('T =', T, end='\n\n')
    
    print('EXAMPLE 4: Mlen 512')
    M = '6bc1bee2 2e409f96 e93d7e11 7393172a ae2d8a57 1e03ac9c 9eb76fac 45af8e51 30c81c46 a35ce411 e5fbc119 1a0a52ef f69f2445 df4f9b17 ad2b417b e66c3710'
    (T, C) = AES_CMAC(M, K)
    print('T =', T)
