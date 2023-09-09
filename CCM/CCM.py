from formatCounterBlock import formatCounterBlock, findM
from AES import encryptAES, convertToHex
from formatInputData import formatInputData, splitMessage, convertHextoBinary
from pprint import pprint
import math


def CCM_Encryption(K: str, N: str, A: str, P: str, Tlen: int) -> str:
    '''Encrpyt the N, A and P with AES128 CCM algorithm with a key K, and a MAC length Tlen'''
    B = splitMessage(formatInputData(N, A, P, Tlen // 8), 128)
    
    Y = list()
    Y.append(encryptAES(convertToHex(int(B[0], 2), 32), K))
    
    Tlen = Tlen // 4
    
    for i in range(1, len(B)):
        Y.append(encryptAES(convertToHex(int(B[i], 2) ^ int(Y[i - 1], 16), 32), K))
    
    T = format(int(convertHextoBinary(Y[-1]).replace(' ', '')[:Tlen * 4], 2), '0' + str(Tlen) + 'X')
    
    print('T:', T)
    
    Ctrs = formatCounterBlock(findM(P), N)
    print('Ctr List:', end=' ')
    pprint(Ctrs)
    
    S_list = list()
    for j in range(0, findM(P) + 1):
        S_list.append(encryptAES(Ctrs[j], K))
    
    print('S List:', end=' ')
    pprint(S_list)
    
    S_str = ''.join(S_list[1:])
    print('S String:', S_str)
    
    
    P = P.replace(' ', '')
    C = convertToHex(int(P, 16) ^ int(S_str[:len(P)], 16), len(P)) + convertToHex(int(T, 16) ^ int(S_list[0][:len(T)], 16), len(T))
    
    print('C:', ' '.join(splitMessage(C, 8)))
    
    return C


def CCM_Decryption(K: str, N: str, A: str, C: str, Tlen: int):
    '''Decryption function for CCM with a provided C ciphertext and K cipher block key.'''
    # Tlen is in bit format, C is in hex format
    Clen = len(C.replace(' ', '')) * 4
    
    if Clen <= Tlen:
        print('INVALID')
        exit()
    
    m = math.ceil((Clen - Tlen) / 128)
    Ctrs = formatCounterBlock(m, N)
   
    S_list = list()
    for j in range(0, m + 1):
        S_list.append(encryptAES(Ctrs[j], K))
    
    S_str = ''.join(S_list[1:])
    
    P = convertToHex(int(C[:((Clen - Tlen) // 4)], 16) ^ int(S_str[:((Clen - Tlen) // 4)], 16), (Clen - Tlen) // 4)
    T = convertToHex(int(C[-(Tlen // 4):], 16) ^ int(S_list[0][:(Tlen // 4)], 16), Tlen // 4)
    
    # Control whether the N, A and P are valid
    
    B = splitMessage(formatInputData(N, A, P, Tlen // 8), 128)
    
    Y = list()
    Y.append(encryptAES(convertToHex(int(B[0], 2), 32), K))
    
    for i in range(1, len(B)):
        Y.append(encryptAES(convertToHex(int(B[i], 2) ^ int(Y[i - 1], 16), 32), K))
    
    print('P:', ' '.join(splitMessage(P, 8)))
    
    print(T.replace(' ', '').upper(), Y[-1][:(Tlen // 4)].replace(' ', '').upper())
    
    if T.replace(' ', '').upper() == Y[-1][:(Tlen // 4)].replace(' ', '').upper():
        print('Decrypted P:', ' '.join(splitMessage(P, 8)))
        return P
    else:
        print('INVALID')

if __name__ == '__main__':
    print('Example 1:')
    K = '40414243 44454647 48494a4b 4c4d4e4f'
    N = '10111213 141516'
    A = '00010203 04050607'
    P = '20212223'
    Tlen = 32
    C = CCM_Encryption(K, N, A, P, Tlen)
    CCM_Decryption(K, N, A, C, Tlen)
    
    print()
    
    print('Example 2:')
    K = '40414243 44454647 48494a4b 4c4d4e4f'
    N = '10111213 14151617'
    A = '00010203 04050607 08090a0b 0c0d0e0f'
    P = '20212223 24252627 28292a2b 2c2d2e2f'
    Tlen = 48
    C = CCM_Encryption(K, N, A, P, Tlen)
    P = CCM_Decryption(K, N, A, C, Tlen)
    
    print()
    
    print('Example 3:')
    K = '40414243 44454647 48494a4b 4c4d4e4f'
    N = '10111213 14151617 18191a1b'
    A = '00010203 04050607 08090a0b 0c0d0e0f 10111213'
    P = '20212223 24252627 28292a2b 2c2d2e2f 30313233 34353637'
    Tlen = 64
    C = CCM_Encryption(K, N, A, P, Tlen)
    P = CCM_Decryption(K, N, A, C, Tlen)
    
