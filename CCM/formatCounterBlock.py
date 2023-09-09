import math, formatInputData
from formatInputData import convertHextoBinary, convertToBinary, findOctetLength, splitMessage


def findM(P: hex) -> int:
    '''Find the m value which will determine the counter number - 1'''
    return math.ceil(len(formatInputData.convertHextoBinary(P).replace(' ', '')) / 128)


def formatCounterBlock(m: int, N: str) -> list:
    '''Return the list of Ctr values'''
    Q_len = 15 - findOctetLength(N) # Calculate the octet length of Q with n
    
    # Try to get Ctr0
    Ctr_list = list()
    for i in range(0, m + 1):
        flags = '00000' + convertToBinary(Q_len - 1, 3)
        N_bin = convertToBinary(int(N.replace(' ', ''), 16), (15 - Q_len) * 8)
        i8q = convertToBinary(i, Q_len * 8)
        Ctr_list.append(format(int(flags + N_bin + i8q, 2), '032X'))
    
    return Ctr_list
    
    
def test():
    # Example 1
    P = '20212223'
    N = '10111213 141516'
    Ctr0 = '07101112 13141516 00000000 00000000'
    Ctr1 = '07101112 13141516 00000000 00000001'
    
    test_results = formatCounterBlock(P, N)
    print('Example 1 - ', end='')
    print('Test Successful') if test_results[0].upper() == Ctr0.replace(' ', '').upper() and test_results[1].upper() == Ctr1.replace(' ', '').upper() else print('Unsuccessful')
    
    P = '20212223 24252627 28292a2b 2c2d2e2f'
    N = '10111213 14151617'
    Ctr0 = '06101112 13141516 17000000 00000000'
    Ctr1 = '06101112 13141516 17000000 00000001'
    test_results = formatCounterBlock(P, N)
    print('Example 2 - ', end='')
    print('Test Successful') if test_results[0].upper() == Ctr0.replace(' ', '').upper() and test_results[1].upper() == Ctr1.replace(' ', '').upper() else print('Unsuccessful')
    
    P = '20212223 24252627 28292a2b 2c2d2e2f 30313233 34353637'
    N = '10111213 14151617 18191A1B'
    Ctr0 = '02101112 13141516 1718191A 1b000000'
    Ctr1 = '02101112 13141516 1718191A 1b000001'
    test_results = formatCounterBlock(P, N)
    print('Example 3 - ', end='')
    print('Test Successful') if test_results[0].upper() == Ctr0.replace(' ', '').upper() and test_results[1].upper() == Ctr1.replace(' ', '').upper() else print('Unsuccessful')
