import TC20_Enc_lib, TC20_Dec_lib
import int_list_lib
import pickle_file

'''
#=================================================================
MITM 
- Meet-in-the-Middle Attack
- Toy Cipher TC20D에 대한 키 전수조사 공격
- TC20D 알고리즘 : TC20을 두번 사용하는 암호
- ct = TC20(TC20(pt, key1), key2)

#=================================================================
pt1 = [1, 2, 3, 4]
mid1 = [208, 72, 44, 125]
ct1 = [156, 101, 28, 237]
pt2 = [4, 3, 2, 1]
mid2 = [142, 212, 64, 245]
ct2 = [59, 108, 107, 113]

ct1 = [156, 101, 28, 237] <- mid1 = [208, 72, 44, 125] <- pt1 = [1, 2, 3, 4]
ct2 = [59, 108, 107, 113] <- mid2 = [142, 212, 64, 245] <- pt2 = [4, 3, 2, 1]

--> pt1, ct1, pt2, ct2를 이용하여 key 전수조사 공격
#==================================================================
'''

#======================================================
# 주어진 평문 pt1에 대하여, 모든 key1 후보로 암호화한 결과를 사전으로 만든다.
# 우연찮게 다른 key1이 같은 mid1을 만들 수 있기때문에 사전으로 만듬
# mid1 <-- E(pt1, key1) <-- pt1(고정)
# 사전 mid_dec = {(mid1, [key1 리스트])}
# 예 : mid_dic[mid1] = [key1 리스트]
def make_enc_dic(pt):
    dic = {}
    print('Making Encryption Dictionary', end='')
    N = 1<<24 # 24bit 키 , N = 2^24
    for idx in range(0,N):
        key = int_list_lib.int2list(idx)
        mid = TC20_Enc_lib.TC20_Enc(pt, key)
        int_mid = int_list_lib.list2int(mid)
        int_key = int_list_lib.list2int(key) #int_key = idx

        if int_mid in dic: # int_mid : 전에 나온적이 있는 값
            dic[int_mid].append(int_key)
        else: # 처음 나온 int_mid
            dic[int_mid] = [int_key]
        if (idx%(1<<18)) == 0:
            print('.', end='')
    
    return dic

#==================================================
# 주어진 키 key1 후보 리스트 중에서 올바른 키가 있는지 찾는다.
# key1 후보들 = [k1, k2, ... ]중에서
# pt2를 암호화하여 ct2를 만든 것을 찾는다. (key2는 고정)
# ct2 <-- E(M, key2) <-- M <-- E(pt2, k1) <-- pt2
def verify_key_candidate_list(key1_list, key2, pt2, ct2):
    flag = False # 후보 없음
    for key1 in key1_list:
        key1_state = int_list_lib.int2list(key1)
        mid2 = TC20_Enc_lib.TC20_Enc(pt2, key1_state)
        ct2_calc = TC20_Enc_lib.TC20_Enc(mid2, key2)
        if ct2_calc == ct2:
            print('\nkey1 = ', key1_state, 'key2 = ',key2)
            flag = True
    
    return flag

#==========================================================
# 공격조건 : (pt1, ct1), (pt2, ct2) 로부터 key1, key2 찾기
#==========================================================
pt1 = [1, 2, 3, 4]
ct1 = [156, 101, 28, 237]
pt2 = [4, 3, 2, 1]
ct2 = [59, 108, 107, 113]

#============================================
# 사전 만들기
mid_dic = make_enc_dic(pt1)
# 사전 파일로 저장하기
pickle_file.save_var_to_file(mid_dic, 'TC20/TC20EncDic.p')
# 사전을 파일에서 가져오기
mid_dic = pickle_file.load_var_from_file('TC20/TC20EncDic.p')
print('Dictionary loaded')

#============================================
N = 1<<22 # key2의 크기 2^24
for idx in range(0, N):
    key2 = int_list_lib.int2list(idx)
    mid1 = TC20_Dec_lib.TC20_Dec(ct1, key2) # ct1을 key2로 복호화
    int_mid1 = int_list_lib.list2int(mid1)

    if int_mid1 in mid_dic:
        list_key1_candidate = mid_dic[int_mid1]
        if len(list_key1_candidate)>0:
            verify_key_candidate_list(list_key1_candidate, key2, pt2, ct2)
    if(idx%(1<<18)) == 0:
        print('.',end='')

print('\n key search completed !!!')