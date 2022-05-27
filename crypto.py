import re
import secrets
import random
import msvcrt
from PyInquirer import prompt #pip install PyInquirer

subkeys = []

mode_question = [
    {
        'type': 'list',
        'name': 'mode',
        'message': 'Select a mode',
        'choices': ['Encrypt', 'Decrypt']
    }]
secret_key_questions = [
    {
        'type': 'password',
        'name': 'secret_key',
        'message': 'Enter the secret key'
    },
    {
        'type': 'password',
        'name': 'secret_key_confirmation',
        'message': 'Confirm the secret key'
    }]

def main():
    #Asking mode
    encrypt = False
    mode = prompt(mode_question)['mode']
    if (mode == 'Encrypt'):
        encrypt = True

    #Getting secret key
    correct = False
    while (not correct):
        secret_key_answers = prompt(secret_key_questions)
        if (len(secret_key_answers['secret_key']) != 0 and secret_key_answers['secret_key'] == secret_key_answers['secret_key_confirmation'] and re.match("[a-zA-Z0-9]| |,", secret_key_answers['secret_key'])):
            correct = True
        else:
            print("The secret key does not match or is invalid, retry\n")
    secret_key = secret_key_answers['secret_key']
    print('\n')

    #Getting the text
    text = ""
    stop = False
    while not stop:
        currchar = msvcrt.getch().decode("utf-8", "replace")
        if CharToInt(currchar) == None:
            stop = True
        else:
            print(currchar, end='', flush=True)
            text += currchar

    #Generating subkeys
    genSubkeys(secret_key)

    print("\nProcessing...")

    #Formatting the text and processing
    processed_text = ""
    if len(text) % 2 != 0:
        text += ' '
    for charindex in range(0, len(text), 2):
        feistel = RunFeistel(text[charindex], text[charindex+1], encrypt) #encrypt is true if the user is encrypting otherwise it's false if decrypting
        processed_text += feistel[0] + feistel[1]
        
    print(processed_text)
    
    return

def CharToInt(chr):
    if re.match("[a-z]", chr):
        return ord(chr) - 97
    if re.match("[A-Z]", chr):
        return ord(chr) - 65 + 26
    if re.match(" ", chr):
        return 52
    if re.match("[0-9]", chr):
        return ord(chr) + 5
    if re.match(",", chr):
        return ord(chr) + 19

def IntToChar(int):
    if (int <= 25):
        return chr(int + 97)
    if (int <= 51):
        return chr(int + 39)
    if (int == 52):
        return ' '
    if (int <= 62):
        return chr(int - 5)
    if (int == 63):
        return ','

def RunFeistel(left, right, encrypt):
    global subkeys

    left = CharToInt(left)
    right = CharToInt(right)

    keyorder = subkeys
    if (encrypt == False):
        keyorder = keyorder[::-1]

    for currsubkey in keyorder:
        functresult = FeistelFunction(right, currsubkey)
        xorresult = int(functresult, base=2) ^ left
        #print (functresult, xorresult, left, right, currsubkey) #debug
        left, right = right, xorresult
        #print(left, right) #debug

    left, right = right, left
    return (IntToChar(left), IntToChar(right), )
    
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
    global subkeys
    subkeys = []
    iteration = 0
    charcount = 0
    for currchar in key:
        random.seed(currchar)
        charcount += random.randint(0, 1000)
    for currchar in key:
        iteration+=1
        random.seed(CharToInt(currchar) + iteration + charcount, version=2)
        subkeys.append(random.randint(0, 63))
        subkeys.append(random.randint(0, 63))

if __name__ == "__main__":
    main()
