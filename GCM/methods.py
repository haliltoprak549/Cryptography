def readableBinary(message: str, X: bin) -> hex:
    '''Convert a binary number into a hexadecimal number with a readable format.'''
    return message + ': ' + ' '.join(splitMessage(convertBinaryToHex(X, len(X) // 4), 8))
    
def readableHex(message: str, X: hex) -> hex:
    '''Convert a binary number into a hexadecimal number with a readable format.'''
    return message + ': ' + ' '.join(splitMessage(X, 8))


def convertToBinary(number: int, bit_number: int) -> bin:
    '''Convert a number in integer format into a binary format with a fixed size with bit_number.'''
    return format(number, '0' + str(bit_number) + 'b') if (number < 2**bit_number and number >= 0) else None

def convertBinaryToHex(X: bin, b: int) -> hex:
    return format(int(X, 2), '0' + str(b) + 'X')


def convertToHex(value: int, b: int) -> hex:
    '''Convert a given integer value into b digit hexadecimal number.'''
    return f"{value:0{b}x}".upper()
    

def convertHexToBinary(X: hex) -> bin:
    '''Convert a hexadecimal number into a binary number ant return it with a readable format.'''
    chunks = splitMessage(X.replace(' ', ''), 2)
    return ''.join([convertToBinary(int(chunk, 16), 8) for chunk in chunks])


def splitMessage(message: str, size: int) -> list:
    '''Split a message into given size blocks and return them as a list.'''
    return [message[i:i+size] for i in range(0, len(message), size)]
    
    
def XOR(X: bin, Y: bin, result_len: int) -> hex:
    '''XOR two binary number strings and return the resulting binary number string with a size of result_len parameter'''
    return convertToBinary(int(X, 2) ^ int(Y, 2), result_len)
    

def rightShift(X: bin) -> bin:
    '''Right shift a binary number string by one bit.'''
    return '0' + X[:-1]
