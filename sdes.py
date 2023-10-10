
PLAINTEXT_LENGTH = 12
KEY_LENGTH = 8

sbox1 = [[0b101, 0b010, 0b001, 0b110, 0b011, 0b100, 0b111, 0b000], [0b001, 0b100, 0b110, 0b010, 0b000, 0b111, 0b101, 0b011]]
sbox2 = [[0b100, 0b000, 0b110, 0b101, 0b111, 0b001, 0b011, 0b010], [0b101, 0b011, 0b000, 0b111, 0b110, 0b010, 0b001, 0b100]]

key = 0b001001101

plaintext = 0b000111011011
plaintext2 =0b101110011011

def pad(binArray, length):
    if(len(binArray) < length):
        return [0]*abs(length - len(binArray)) + binArray
    return binArray

def binToBinArray(binNumber, padding):
    return pad([int(i) for i in bin(binNumber)[2:]], padding)

def BinArrayTobin(binArray):
    return int("".join(map(str, binArray)), 2)


# BIT 123456
# EXPANDED: 12434356

def expansion(input):
    output = [input[0], input[1], input[3], input[2], input[3], input[2], input[4], input[5]]
    return output

    

def keySchedule(key, round):
    _key = []
    for i in range(round, KEY_LENGTH + round):
        _key.append(binToBinArray(key, KEY_LENGTH + 1)[i % (KEY_LENGTH + 1)])
    return _key

def xor(val1, val2):
    result = []
    if(len(val1) == len(val2)):
        for i in range(0, len(val1)):
            result.append(val1[i] ^ val2[i])
    return result

def feistel(input, key):
    expanded = expansion(input)
    #print(f"Expanded: {expanded}")
    xored = xor(expanded, key)
    
    xoredLeft = xored[0:4]
    xoredRight = xored[4:]
    #print(f"XOR: {(xored)}")
    print(f"SBOX1: ({xoredLeft[0]}, {BinArrayTobin(xoredLeft[1:])})")
    print(f"SBOX2: ({xoredRight[0]}, {BinArrayTobin(xoredRight[1:])})")
    result = binToBinArray((sbox1[xoredLeft[0]][BinArrayTobin(xoredLeft[1:])] << 3) | sbox2[xoredRight[0]][BinArrayTobin(xoredRight[1:])], 6)
    print(f"RESULT: {result}")
    return result




def sdesRound(halfLeft, halfRight, round):
    
    outFeistel = feistel(halfRight, keySchedule(key, round))

    return (halfRight, xor(halfLeft, outFeistel))

def sdes(input, maxRound):
    halfRight = binToBinArray(input & (0b000000111111), PLAINTEXT_LENGTH//2)
    halfLeft = binToBinArray((input & (0b111111000000)) >> PLAINTEXT_LENGTH//2, PLAINTEXT_LENGTH//2)
    output = 0
    for i in range(1, maxRound + 1):
        print(f"[{i}] Left: {halfLeft} Right: {halfRight} Key: {keySchedule(key, i)}")
        output = sdesRound(halfLeft, halfRight, i)
        print(f"[{i}] Output from round: {output}")
        halfLeft = output[0]
        halfRight = output[1]
    return output

result = sdes(plaintext2, 3)


print(f"SDES Result {result}")