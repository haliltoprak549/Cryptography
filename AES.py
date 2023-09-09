from pprint import pprint


def splitMessage(message: str) -> list:
    '''Split the message into bytes.'''
    message = message.upper().replace(' ', '')
    return [message[i:i+2] for i in range(0, len(message), 2)] # 128-bit message split into bytes (8 bit) = 16 elements


def keyExpansion(key: str, j: int):
    '''Generate the round keys from the initial key'''
    key = splitMessage(key.upper().replace(' ', '')) # Split the key into its bytes
    words = ['00000000'] * 44
    
    Rc = {1: '01', 2: '02', 3: '04', 4: '08', 5: '10', 6: '20', 7: '40', 8: '80', 9: '1B', 10: '36'}
    Rcon = {key: old_value + '000000' for key, old_value in Rc.items()}
    print('Rcon: ', Rcon) # Debug

    for i in range(0, 4):
        words[i] = ''.join([key[4 * i], key[4 * i + 1], key[4 * i + 2], key[4 * i + 3]])

    for i in range(4, 44):
        temp = words[i - 1]
        if i % 4 == 0:
            temp = int(subBytes(RotWord(temp)), 16) ^ int(Rcon[i // 4], 16)
            # Perform one byte circular shift and substitute bytes
            words[i] = convertToHex((int(words[i - 4], 16) ^ temp), 8)
        else:
            words[i] = convertToHex((int(words[i - 4], 16) ^ int(temp, 16)), 8)
    
    k = 0
    grouped = list()
    for i in range(len(words) // 4):
        grouped.append(words[k] + words[k + 1] + words[k + 2] + words[k + 3])
        k = k + 4
    
    return grouped


def subBytes(message: str) -> str:
    '''Substitute bytes, change them to another value in according to lookup table.'''
    
    # Split the message into bytes
    chunks = splitMessage(message)

    # S-Box substitution lookup table in dictionary format
    S_BOX1 = { "00": "63", "01": "7C", "02": "77", "03": "7B", "04": "F2", "05": "6B", "06": "6F", "07": "C5", "08": "30", "09": "01", "0A": "67", "0B": "2B", "0C": "FE", "0D": "D7", "0E": "AB", "0F": "76", "10": "CA", "11": "82", "12": "C9", "13": "7D", "14": "FA", "15": "59", "16": "47", "17": "F0", "18": "AD", "19": "D4", "1A": "A2", "1B": "AF", "1C": "9C", "1D": "A4", "1E": "72", "1F": "C0", "20": "B7", "21": "FD", "22": "93", "23": "26", "24": "36", "25": "3F", "26": "F7", "27": "CC", "28": "34", "29": "A5", "2A": "E5", "2B": "F1", "2C": "71", "2D": "D8", "2E": "31", "2F": "15", "30": "04", "31": "C7", "32": "23", "33": "C3", "34": "18", "35": "96", "36": "05", "37": "9A", "38": "07", "39": "12", "3A": "80", "3B": "E2", "3C": "EB", "3D": "27", "3E": "B2", "3F": "75", "40": "09", "41": "83", "42": "2C", "43": "1A", "44": "1B", "45": "6E", "46": "5A", "47": "A0", "48": "52", "49": "3B", "4A": "D6", "4B": "B3", "4C": "29", "4D": "E3", "4E": "2F", "4F": "84", "50": "53", "51": "D1", "52": "00", "53": "ED", "54": "20", "55": "FC", "56": "B1", "57": "5B", "58": "6A", "59": "CB", "5A": "BE", "5B": "39", "5C": "4A", "5D": "4C", "5E": "58", "5F": "CF", "60": "D0", "61": "EF", "62": "AA", "63": "FB", "64": "43", "65": "4D", "66": "33", "67": "85", "68": "45", "69": "F9", "6A": "02", "6B": "7F", "6C": "50", "6D": "3C", "6E": "9F", "6F": "A8", "70": "51", "71": "A3", "72": "40", "73": "8F"
    }
    
    S_BOX2 = {"74": "92", "75": "9D", "76": "38", "77": "F5", "78": "BC", "79": "B6", "7A": "DA", "7B": "21", "7C": "10", "7D": "FF", "7E": "F3", "7F": "D2", "80": "CD", "81": "0C", "82": "13", "83": "EC", "84": "5F", "85": "97", "86": "44", "87": "17", "88": "C4", "89": "A7", "8A": "7E", "8B": "3D", "8C": "64", "8D": "5D", "8E": "19", "8F": "73", "90": "60", "91": "81", "92": "4F", "93": "DC", "94": "22", "95": "2A", "96": "90", "97": "88", "98": "46", "99": "EE", "9A": "B8", "9B": "14", "9C": "DE", "9D": "5E", "9E": "0B", "9F": "DB", "A0": "E0", "A1": "32", "A2": "3A", "A3": "0A", "A4": "49", "A5": "06", "A6": "24", "A7": "5C", "A8": "C2", "A9": "D3", "AA": "AC", "AB": "62", "AC": "91", "AD": "95", "AE": "E4", "AF": "79", "B0": "E7", "B1": "C8", "B2": "37", "B3": "6D", "B4": "8D", "B5": "D5", "B6": "4E", "B7": "A9", "B8": "6C", "B9": "56", "BA": "F4", "BB": "EA", "BC": "65", "BD": "7A", "BE": "AE", "BF": "08", "C0": "BA", "C1": "78", "C2": "25", "C3": "2E", "C4": "1C", "C5": "A6", "C6": "B4", "C7": "C6", "C8": "E8", "C9": "DD", "CA": "74", "CB": "1F", "CC": "4B", "CD": "BD", "CE": "8B", "CF": "8A", "D0": "70", "D1": "3E", "D2": "B5", "D3": "66", "D4": "48", "D5": "03", "D6": "F6", "D7": "0E", "D8": "61", "D9": "35", "DA": "57", "DB": "B9", "DC": "86", "DD": "C1", "DE": "1D", "DF": "9E", "E0": "E1", "E1": "F8", "E2": "98", "E3": "11", "E4": "69", "E5": "D9", "E6": "8E", "E7": "94", "E8": "9B", "E9": "1E", "EA": "87", "EB": "E9", "EC": "CE", "ED": "55", "EE": "28", "EF": "DF", "F0": "8C", "F1": "A1", "F2": "89", "F3": "0D", "F4": "BF", "F5": "E6", "F6": "42", "F7": "68", "F8": "41", "F9": "99", "FA": "2D", "FB": "0F", "FC": "B0", "FD": "54", "FE": "BB", "FF": "16"
    }

    substitued_chunks = [(S_BOX1[x] if x in S_BOX1.keys() else S_BOX2[x]) for x in chunks]
    return ''.join(substitued_chunks)
    

def shiftRows(message: str) -> list:
    '''Shift rows with an offset of 0 for the first row, 1 for the second row etc. to left.'''
    chunks = splitMessage(message)
    state_matrix = list()
   
    for i in range(0, 4, 1): # Turn rows into a list
        temp_list = list()
        for j in range(i, i+13, 4):
            temp_list.append(chunks[j])
        state_matrix.append(temp_list)
    
    for i in range(1, 4):  # Start from the second row
        state_matrix[i] = state_matrix[i][i:] + state_matrix[i][:i] # Shift the rows
    
    return state_matrix


def mixColumns(state: list):
    
    columns = list()
    for i in range(4):
        column = list()
        for j in range(4):
            column.append(state[j][i])
        columns.append(column)
    
    new_columns = list()
    for column in columns:
        a = int(column[0], 16)
        b = int(column[1], 16)
        c = int(column[2], 16)
        d = int(column[3], 16)
    
        c0 = convertToHex(gmul(a, 2) ^ gmul(b, 3) ^ gmul(c, 1) ^ gmul(d, 1), 2)
        c1 = convertToHex(gmul(a, 1) ^ gmul(b, 2) ^ gmul(c, 3) ^ gmul(d, 1), 2)
        c2 = convertToHex(gmul(a, 1) ^ gmul(b, 1) ^ gmul(c, 2) ^ gmul(d, 3), 2)
        c3 = convertToHex(gmul(a, 3) ^ gmul(b, 1) ^ gmul(c, 1) ^ gmul(d, 2), 2)
        
        new_columns.append([c0, c1, c2, c3])
    
    return new_columns


def gmul(a: int, b: int) -> int:
    if b == 1:
        return a
    tmp = (a << 1) & 0xff
    if b == 2:
        return tmp if a < 128 else tmp ^ 0x1b
    if b == 3:
        return gmul(a, 2) ^ a


def addRoundKey(state: list, roundKey: str):
    '''XOR the message with round key, message in column list format'''
    return convertToHex(int(''.join([''.join(column) for column in state]), 16) ^ int(roundKey, 16), 32)


def addRoundKeyWithStr(message: str, roundKey: str):
    '''XOR the message with round key, message in string format.'''
    return convertToHex(int(message, 16) ^ int(roundKey, 16), 32)


def convert2x2toStrByColumns(list4x4: list) -> str:
    return ''.join([''.join(row) for row in list4x4])


def convert2x2toStrByRows(list4x4: list) -> str:
    list_str = list()
    for i in range(0, 4): # column
        for j in range(0, 4): # row
            list_str.append(list4x4[j][i])
    return ''.join(list_str)


def RotWord(word: str) -> str:
    '''Perform one-byte circular shift on a word'''
    word_array = splitMessage(word)
    word_array.append(word_array.pop(0))
    return ''.join(word_array)


def convertToHex(value: int, b: int) -> str:
    '''Convert a given integer value into b digit hexadecimal number.'''
    return f"{value:0{b}x}".upper()


def encryptAES(message: str, key: str, number_of_rounds: int):
    '''Main function which takes the '''
    message = message.replace(' ', '').upper()
    round_keys = keyExpansion(key, 1)
    print('Expanded key: ', ' '.join(round_keys), end='\n\n')
    
    print('Initial Round')
    print('Input to Initial Round: ', message)
    print('Used subkey: ', round_keys[0])
    message = addRoundKeyWithStr(message, round_keys[0])
    print('After mix with key: ', message, end='\n\n')
    
    mix = message # starting with message
    for i in range(1, number_of_rounds + 1):
        print('Round ', i)
        print('Input to Round ', i, ': ', mix)
        
        sbox = subBytes(mix)
        
        print('After S-Box: ', sbox)
        
        permutation = shiftRows(sbox)
        
        print('After permutation: ', convert2x2toStrByRows(permutation))
        
        if i != number_of_rounds:
            mult = mixColumns(permutation)
            print('After mult: ', convert2x2toStrByColumns(mult))
            
            print('Used subkey: ', round_keys[i])
            mix = addRoundKey(mult, round_keys[i])
            
            print('After mix with key: ', mix, end='\n\n')
        else:
            print('Used subkey: ', round_keys[i])
            transposed_permutation = [[row[i] for row in permutation] for i in range(4)]
            mix = addRoundKey(transposed_permutation, round_keys[i])
            print('After mix with key: ', mix, end='\n\n')
        
    return mix


if __name__ == '__main__':
    key = 'E8E9EAEBEDEEEFF0F2F3F4F5F7F8F9FA'
    message = '014BAF2278A69D331D5180103643E99A'
    number_of_rounds = 10
    
    result = encryptAES(message, key, number_of_rounds)
    print('Encrypted Result: ', result)
