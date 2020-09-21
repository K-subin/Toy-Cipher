import TC20_Enc_lib
 
#--- TF20 라운드 암호화 함수
#--- (L, R) --> (L', R') = (F(L, rkey)^R, L)
def Enc_Round(inL, inR, rkey):
    outL = outR = [0]*4
    outR = inL
    outF = TC20_Enc_lib.Enc_Round(inL, rkey)
    for i in range(len(outF)):
        outL[i] = outF[i] ^ inR[i]
    return outL, outR

#--- TF20 암호화 (TF20_Enc1 == TF20_Enc2)
def TF20_Enc_Dec(in_state, key):
    inL = in_state[:4]
    inR = in_state[4:]
    numRound = 16

    #final swap
    inL, inR = inR, inL

    for i in range (0, numRound):
        inL, inR = Enc_Round(inL, inR, key)
        
    out_state = inL + inR
    return out_state

# 라운드 키가 동일하다면 복호화는 암호화와 똑같다.

def main():
    message = 'ABCDEFGH'
    in_state = [ord(ch) for ch in message]
    key = [0, 1, 2, 3]
    Encrypted = TF20_Enc_Dec(in_state, key)

    Decrypted = TF20_Enc_Dec(Encrypted, key)
    list1 = [chr(x) for x in Decrypted]
    recovered_msg = ''.join(list1)

    print('message =', message)
    print('in_state =', in_state)
    print('Encrypted =', Encrypted)
    print('decrypted =', Decrypted)
    print('recovered_msg =', recovered_msg)

# 라이브러리 파일인데 실행하면서 작성하기
# 라이브러리로 호출될때는 실행되지 않음
# 파일을 실행하면 main()함수가 호출됨

if __name__ == '__main__': 
    main()