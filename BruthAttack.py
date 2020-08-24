import TC20_Enc_lib, TC20_Dec_lib
import int_list_lib

#---------------------------
# 준비 : 평문과 키로 암호문 구하기 
# given_pt = [65, 66, 67, 68]
# key = [0, 1, 2, 3]
# ct = TC20_Enc_lib.TC20_Enc(given_pt, key)
# print(ct)

#----------------------------
# 평문과 암호문을 이용해 키 추측하기
# 전수조사 공격

given_pt = [65, 66, 67, 68]
given_ct = [246, 31, 30, 133]
KeySize = 1 << 22   # 키 20bit만 전수조사 (최대 : 32bit)
print('plain text :', given_pt)
print('cipher text :', given_ct)

print('key searching', end='')
for idx in range(0, KeySize):
    guess_key = int_list_lib.int2list(idx)
    pt = TC20_Dec_lib.TC20_Dec(given_ct, guess_key)
    if pt == given_pt:
        print('\nkey = ', guess_key)
        break
    if(idx % (1<<15)) == 0:
        print('.', end='')