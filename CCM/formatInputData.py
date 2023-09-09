from pprint import pprint
import math


def splitMessage(message: str, size: int) -> list:
    '''Split a message into two digits and return it as a list.'''
    return [message[i:i+size] for i in range(0, len(message), size)]


def convertHextoBinary(hex_str: str) -> str:
    '''Convert a hexadecimal number into a binary number ant return it with a readable format.'''
    chunks = splitMessage(hex_str.replace(' ', ''), 2)
    return ' '.join([convertToBinary(int(chunk, 16), 8) for chunk in chunks])


def findOctetLength(hex_str: str) -> int:
    '''Find and return the octet length of a hexadecimal string'''
    return len(hex_str.replace(' ', '')) // 2


def convertToBinary(number: int, bit_number: int) -> str:
    '''Convert a number in integer format into a binary format with a fixed size with bit_number.'''
    return format(number, '0' + str(bit_number) + 'b') if (number < 2**bit_number and number >= 0) else None


def paddingToRight(bin_str: str, bin_number: int) -> str:
    '''Convert a binary string into a binary number with a desired length, but add padding to the right.'''
    while len(bin_str) < bin_number:
        bin_str += '0'
    
    return bin_str


def formatB0(N: str, A: str, P: str, Tlen: int):
    # Find q (Octet length of Q) with using equation 'n+q = 15'
    Qlen = 15 - findOctetLength(N)
    
    # Reserved bit
    B0_flags_7 = '0'
    
    # Adata bit '0' if there is no Associated Data, '1' if there is
    B0_flags_6 = '0' if A == '' else '1'
    
    # Calculate the 012 bits of B0 with q
    B0_flags_210 = convertToBinary(Qlen - 1, 3)
    
    # Calculate the 345 bits of B0 with t
    B0_flags_543 = convertToBinary((Tlen - 2) // 2, 3)
    
    # Concetanete all values and get B0 flags Octet
    B0_flags = B0_flags_7 + B0_flags_6 + B0_flags_543 + B0_flags_210
    
    # Convert N into binary format and fix it with size 15 - q bits
    N_bin = convertToBinary(int(N.replace(' ', ''), 16), (15 - Qlen) * 8)
    
    
    Q_bin = convertToBinary(findOctetLength(P), Qlen * 8)
    
    B0 = B0_flags + N_bin + Q_bin
    
    return B0


def formatAssocData(A: str) -> str:
    # Calculate the octet length of Associated Data
    a = findOctetLength(A)
    
    if a > 0 and a < 2**16 - 2**8:
        # [a]16
        a = convertToBinary(a, 16)
    elif a >= 2**16 - 2**8 and a < 2**32:
        # 0xFF || 0xFE || [a]32
        a = ('1111 1111' + '1111 1110').replace(' ', '') + convertToBinary(a, 32)
    elif a >= 2**32 and a < 2**64:
        # 0xFF || 0xFF || [a]64
        a = ('1111 1111' + '1111 1111').replace(' ', '') + convertToBinary(a, 64)
    
    a_combined = a + convertHextoBinary(A).replace(' ', '')
    a_bin_len = math.ceil(len(convertHextoBinary(A).replace(' ', '') + a) / 128) * 8 * 16
    
    return paddingToRight(a_combined, a_bin_len)


def formatPayload(P: str) -> str:
    '''Format the payload'''
    p_bin_len = math.ceil(findOctetLength(P) / 16) * 16 * 8
    p_bin = convertHextoBinary(P).replace(' ', '')
    
    return paddingToRight(p_bin, p_bin_len)


def formatInputData(N: str, A: str, P: str, Tlen: int):
    '''Generate B with parameters N, A, P and Tlen'''
    return formatB0(N, A, P, Tlen) + formatAssocData(A) + formatPayload(P)


# Run only if this file is executed directly
def test():
    # TEST AREA (ENTER THE VALUES THAT YOU WANT TO TEST)
    K = '40414243 44454647 48494a4b 4c4d4e4f'
    N = '10111213 14151617 18191a1b'
    A = '00010203 04050607 08090a0b 0c0d0e0f 10111213'
    P = '20212223 24252627 28292a2b 2c2d2e2f 30313233 34353637'
    Tlen = 8
    
    test_result_b = convertHextoBinary('5a101112 13141516 1718191a 1b000018 00140001 02030405 06070809 0a0b0c0d 0e0f1011 12130000 00000000 00000000 20212223 24252627 28292a2b 2c2d2e2f 30313233 34353637 00000000 00000000')
    print('For test purposes, B should be:\n' + test_result_b + '\n')
    
    foundB = formatInputData(N, A, P, Tlen)
    
    print('B Found correctly.') if test_result_b.replace(' ', '') == foundB.replace(' ', '') else print('Wrong result.')
