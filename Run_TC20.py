import TC20_Enc_lib
import TC20_Dec_lib
import random

message = 'Hello, nice to meet you!' #24byte

#----- random key generation
key = []
for i in range(4): 
    key.append(random.randrange(256)) # Sbox length : 256

print('key =', key)

#----- split
msg_split = [ message[i:i+4] for i in range(0, len(message), 4) ] # message를 4byte씩 나누기 (message length : 4byte)

#----- Encrypt
input_state, output_state, ciphertext, plaintext = [0]*len(msg_split), [0]*len(msg_split), [], [] # 초기화
for i in range(len(msg_split)): 
    input_state[i] = [ ord(ch) for ch in msg_split[i] ] # 문자를 아스키 코드 값으로 변환
    output_state[i] = [ item for item in TC20_Enc_lib.TC20_Enc(input_state[i], key) ] # encrypt
    plaintext += input_state[i] # 4byte씩 나눈 것을 합치기
    ciphertext += output_state[i] # 4byte씩 나눈 것을 합치기

print('message =', message)
print('plaintext =', plaintext)
print('ciphertext =', ciphertext)

#----- Decrypt
cipher_split = [ ciphertext[i:i+4] for i in range(0, len(ciphertext), 4) ] # ciphertext를 4byte씩 나누기

output_state, decrypttext,recoveredtext = [0]*len(cipher_split), [], '' # 초기화
for i in range(len(cipher_split)):
    output_state[i] = [item for item in TC20_Dec_lib.TC20_Dec(cipher_split[i], key)]
    decrypttext += output_state[i] # 4byte씩 나눈 것을 합치기
    recoveredtext += ''.join([chr(item) for item in output_state[i]]) # 아스키코드를 문자로 변환해서 합치기

print('decrypttext =', decrypttext)
print('recoveredtext =', recoveredtext)
