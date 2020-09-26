import re
import secrets
import random

subkeys = []


def main():
    genSubkeys("aaa")
    #genSBox()
    #print("subkeys", subkeys)
    #print(FeistelStep(*(1, 2, ), 3))


def CharToInt(chr):
    if re.match("[a-z]", chr):
        return ord(chr) - 97
    if re.match("[A-Z]", chr):
        return ord(chr) - 65 + 26
    if re.match(" ", chr):
        return 52

def IntToChar(int):
    if (int <= 25):
        return chr(int + 97)
    if (int <= 51):
        return chr(int + 39)
    if (int == 52):
        return ' '



def FeistelStep(left, right, subkey):
    newleft = right
    newright = 0



    return (newleft, newright, )
    

def FeistelFunction(number, key):
    total = format(number, "06b") + format(key, "06b") #12bit number composed by the number and the key
    # xxxx 0000 0000 total[:4]
    # 0000 xxxx 0000 total[4:8:]
    # 0000 0000 xxxx total[8:] 
    parts = [total[:4], total[4:8:], total[8:]] #splitting total in 3 equal 4bit parts
    sboxes = [ #3 sboxes (for each part)
        [['110110', '010010', '010101', '011010'], ['111100', '110110', '100011', '010101'], ['100000', '011001', '111011', '110001'], ['010000', '000011', '010110', '000001']],
        [['010110', '110010', '100000', '010000'], ['101000', '101101', '010100', '101110'], ['001001', '101010', '010011', '000100'], ['001001', '111011', '111000', '010110']],
        [['100100', '010110', '010011', '110000'], ['100001', '010011', '110001', '100100'], ['001101', '011101', '110110', '111000'], ['010111', '000100', '100000', '110110']]
    ]

    for i in range(3): #swapping parts with their S-box results
        external = parts[i][0] + parts[i][3:]   #x00x
        middle = parts[i][1:3:]                 #0xx0

        parts[i] = sboxes[i][int(external, base=2)][int(middle, base=2)]
        # print(external, middle, parts[i])
    # print(total)

    sump0p1 = (int(parts[0], base=2) + int(parts[1], base=2)) % 2**6 # part0 + part1 modulo 2^6
    result = format(sump0p1 ^ int(parts[2], base=2), "06b") #(part0 + part1) xor part3

    return result

def genSBox():
    sbox = [ [ 0 for i in range(4) ] for j in range(4) ]
    for i in range(4):
        for k in range(4):
            sbox[i][k] = format(secrets.randbits(6), "06b")
    print(sbox)
    return

def genSubkeys(key):
    iteration = 0
    for currchar in key:
        currbin = format(CharToInt(currchar), "06b")
        random.seed(CharToInt(currchar) + iteration, version=2)
        print(random.randint(0, 63))
        iteration+=2




if __name__ == "__main__":
    main()
