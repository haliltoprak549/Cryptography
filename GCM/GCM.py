from methods import convertToBinary, convertHexToBinary, convertBinaryToHex, splitMessage, XOR, rightShift, readableBinary, readableHex
from AES import encryptAES
from pprint import pprint
import math


def inc(X: bin, s: int) -> bin:
    '''Incrementing function for GCM. The function increments the right-most s bits of the string, regarded as the binary representation of an integer, modulo 2^s; the remaining, left-most len(X)-s bits remain unchanged.'''
    X = X.replace(' ', '') # Remove the possible spaces
    return X[:(len(X) - s)] + convertToBinary((int(X[-s:], 2) + 1) % 2**s, s)


def multiplyBlocks(X: bin, Y: hex) -> bin:
    '''Return the result of a block multiplication operation on two 128-bit blocks.'''
    X = X.replace(' ', '') # Remove the possible spaces on X block
    Y = convertHexToBinary(Y.replace(' ', '')) # Remove the possible spaces on Y block and convert hex to binary
    x = splitMessage(X, 1) # Split the X binary number into bits list
    
    # Create a Z list and define the first item of Z as 0^128
    Z = list()
    Z.append('0' * 128)
    
    # Create a V list and define the first item of V as Y
    V = list()
    V.append(Y)
    
    # R constant
    R = '11100001' + ('0' * 120)
    
    for i in range (0, 128):
        Z.append(Z[i] if x[i] == '0' else XOR(Z[i], V[i], result_len = 128))
        V.append(rightShift(V[i]) if V[i][-1] == '0' else XOR(rightShift(V[i]), R, result_len = 128))
        
    return Z[-1]


def GHASH(X: bin, H: hex) -> bin:
    '''GHASH function with parameters of X binary number which has unknown bits and H which has 32 nibble'''
    x = splitMessage(X, 128)
    
    Y = list()
    Y.append('0' * 128)
    
    for i in range(1, len(x) + 1):
        Y.append(multiplyBlocks(XOR(Y[i - 1], x[i - 1], result_len = 128), H))
    
    return Y[-1]


def GCTR(ICB: bin, X: bin, K: hex) -> bin:
    '''GCTR function'''
    
    if X == '':
        return ''

    # Calculate how many block X contains
    n = math.ceil(len(X) / 128)
    
    # Split the message into blocks, last element Xn* may not be a complete block
    x_list = splitMessage(X, 128)
    
    CB = list()
    CB.append(ICB)
    
    for i in range(1, n):
        CB.append(inc(CB[i - 1], 32))
    
    # Debug
    # print('CB list')
    # pprint([readableBinary('CB', item) for item in CB])
       
    Y = list()
    for i in range(0, n - 1):
        Y.append(XOR(x_list[i], convertHexToBinary(encryptAES(convertBinaryToHex(CB[i], 32), K)), 128))

    Y.append(XOR(x_list[-1], convertHexToBinary(encryptAES(convertBinaryToHex(CB[-1], 32), K))[:(len(x_list[-1]))], result_len = len(x_list[-1])))
    
    # Debug
    # print('Y list')
    # pprint([readableBinary('Y', item) for item in Y])
    
    return ''.join(Y)


def GCM_Encryption(IV: hex, P: hex, A: hex, K: hex, t: int) -> list:
    '''GCM Authentication Encryption Function'''
    IV = convertHexToBinary(IV) # Convert IV into binary to perform operations on
    
    H = encryptAES('0' * 32, K) # gives a 32 nibble hex number
    
    if len(IV) == 96: # If it is a 24 nibble hex number
        J0 = IV + ('0' * 31) + '1'
    else:
        s = 128 * math.ceil(len(IV) / 128) - len(IV)
        J0 = GHASH(IV + ('0' * (s + 64)) + convertToBinary(len(IV), 64), H)
    
    print(readableHex('H', H)) # Debug
    print(readableBinary('J0', J0)) # Debug
    
    C = GCTR(inc(J0, 32), convertHexToBinary(P), K)
    
    A = convertHexToBinary(A)
    
    u = 128 * math.ceil(len(C) / 128) - len(C)
    v = 128 * math.ceil(len(A) / 128) - len(A)
    
    S = GHASH(A + ('0' * v) + C + ('0' * u) + convertToBinary(len(A), 64) + convertToBinary(len(C), 64), H)

    print(readableBinary('S', S)) # Debug
    
    T = GCTR(J0, S, K)[:t]
    
    if C != '':
        return [convertBinaryToHex(C, 32), convertBinaryToHex(T, t // 4)]
    else:
        return ['', convertBinaryToHex(T, t // 4)]
    

def GCM_Decryption(IV: hex, C: hex, A: hex, T: hex, K: hex, t: int) -> str:
    '''Decrypts a ciphertext using IV, authentication tag and block cipher key'''
    # check the bit length requirements
    
    IV = convertHexToBinary(IV.replace(' ', '').upper())
    C = convertHexToBinary(C.replace(' ', '').upper())
    A = convertHexToBinary(A.replace(' ', '').upper())
    T = T.replace(' ', '').upper()
    K = K.replace(' ', '').upper()
    
    H = encryptAES('0' * 32, K) # Outputs a hexadecimal ciphertext
    
    if len(IV) == 96:
        J0 = IV + ('0' * 31) + '1'
    else:
        s = 128 * math.ceil(len(IV) / 128) - len(IV)
        J0 = GHASH(IV + ('0' * (s + 64)) + convertToBinary(len(IV), 64), H)
    
    P = GCTR(inc(J0, 32), C, K)
    
    u = 128 * math.ceil(len(C) / 128) - len(C)
    v = 128 * math.ceil(len(A) / 128) - len(A)
    
    S = GHASH(A + ('0' * v) + C + ('0' * u) + convertToBinary(len(A), 64) + convertToBinary(len(C), 64), H)
    
    T_ = convertBinaryToHex(GCTR(J0, S, K)[:t], t // 4)
    
    if T_ == T:
        return P
    else:
        print('FAIL')
        return 'FAIL'


def test(ex_num, K, IV, AAD, P, Tlen):
    print(f'Example #{ex_num}:')
    
    (C, T) = GCM_Encryption(IV, P, AAD, K, Tlen)
    
    if C == '':
        print('C: <empty>')
    else:
        print(readableHex('C', C))
        
    print(readableHex('Tag', T))
    
    decrypted_P = GCM_Decryption(IV, C, AAD, T, K, Tlen)
    
    if P == '':
        print('Decrypted P: <empty>')
    else:
        print(readableBinary('Decrypted P', decrypted_P))
    print()


if __name__ == '__main__':
    
    # Example #1
    K = 'FEFFE992 8665731C 6D6A8F94 67308308'
    IV = 'CAFEBABE FACEDBAD DECAF888'
    A = ''
    P = ''
    Tlen = 128
    test(1, K, IV, A, P, Tlen)
        
    # Example #2
    K = 'FEFFE992 8665731C 6D6A8F94 67308308'
    IV = 'CAFEBABE FACEDBAD DECAF888'
    A = ''
    P = 'D9313225 F88406E5 A55909C5 AFF5269A 86A7A953 1534F7DA 2E4C303D 8A318A72 1C3C0C95 95680953 2FCF0E24 49A6B525 B16AEDF5 AA0DE657 BA637B39 1AAFD255'
    Tlen = 128
    test(2, K, IV, A, P, Tlen)
    
    # Example #3
    K = 'FEFFE992 8665731C 6D6A8F94 67308308'
    IV = 'CAFEBABE FACEDBAD DECAF888'
    A = '3AD77BB4 0D7A3660 A89ECAF3 2466EF97 F5D3D585 03B9699D E785895A 96FDBAAF 43B1CD7F 598ECE23 881B00E3 ED030688 7B0C785E 27E8AD3F 82232071 04725DD4'
    P = ''
    Tlen = 128
    test(3, K, IV, A, P, Tlen)
    
    # Example #4
    K = 'FEFFE992 8665731C 6D6A8F94 67308308'
    IV = 'CAFEBABE FACEDBAD DECAF888'
    A = '3AD77BB4 0D7A3660 A89ECAF3 2466EF97 F5D3D585 03B9699D E785895A 96FDBAAF 43B1CD7F 598ECE23 881B00E3 ED030688 7B0C785E 27E8AD3F 82232071 04725DD4'
    P = 'D9313225 F88406E5 A55909C5 AFF5269A 86A7A953 1534F7DA 2E4C303D 8A318A72 1C3C0C95 95680953 2FCF0E24 49A6B525 B16AEDF5 AA0DE657 BA637B39 1AAFD255'
    Tlen = 128
    test(4, K, IV, A, P, Tlen)
    
    # Example #5
    K = 'FEFFE992 8665731C 6D6A8F94 67308308'
    IV = 'CAFEBABE FACEDBAD DECAF888'
    A = '3AD77BB4 0D7A3660 A89ECAF3 2466EF97 F5D3D585'
    P = 'D9313225 F88406E5 A55909C5 AFF5269A 86A7A953 1534F7DA 2E4C303D 8A318A72 1C3C0C95 95680953 2FCF0E24 49A6B525 B16AEDF5 AA0DE657 BA637B39'
    Tlen = 128
    test(5, K, IV, A, P, Tlen)
    
    # Example #6
    K = 'FEFFE992 8665731C 6D6A8F94 67308308'
    IV = 'CAFEBABE FACEDBAD DECAF888'
    A = '3AD77BB4 0D7A3660 A89ECAF3 2466EF97 F5D3D585'
    P = 'D9313225 F88406E5 A55909C5 AFF5269A 86A7A953 1534F7DA 2E4C303D 8A318A72 1C3C0C95 95680953 2FCF0E24 49A6B525 B16AEDF5 AA0DE657 BA637B39'
    Tlen = 96
    test(6, K, IV, A, P, Tlen)
    
    # Example from gcmEncryptExtIV128.rsp
    K = 'b95eb8c0a45da1eed07e55f243fdac77'
    IV = '85e3ef18efe883e1298f2f1e713599479e63db5bce2f88097d1c1f1a68284764d9b73a0e9990ef33c5cc68cc3eb607cf7bd483e55c53d3a74b50f5375de7c7fae5ea0e12a96f3f77c69d4d7dd62abaf8cc189e03aec29d39933cf5bfc766a202a46ba20d02b6e4ab0d3a0fe1fd658350ac5971b4ecf6b123ce2b526f58ab7652'
    A = 'ec3265d0ca6795b984f4cbb71721e38f62cd5d3c'
    P = '1da1449bac0339a086bd8f0e9756993a'
    Tlen = 120
    test(7, K, IV, A, P, Tlen)
