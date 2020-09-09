import TC20_Enc_lib, TC20_Dec_lib
import pickle_file # 변수 저장
import int_list_lib
import random
import copy # 딮 카피 (깊은 복사)

#-- TC20 with 24 bit key
# PT = [*, *, *, *] --> CT = [*, *, *, *] 
# key =  [0, *, *, *]

#-- 키 크기, TMTO 테이블 크기 (키크기 = 행크기 * 열크기)
key_bit = 24   # key = [0, *, *, *]

#==========================================
# X_{j+1} = E(P0, X_{j})  # key bit = block size
# X_{j+1} = R(E(P0, X_{j})) # R : 32bit -> 24bit
# SP = X0(key) -> X1 -> X2 -> ... -> Xt = EP
#===========================================

#==========================================
# R : 32bit -> 24bit
# 암호문 [a, b, c, d] --> 암호키 [0, b, c, d]
def R(ct):
    #next_key = ct (ct의 내용이 함께 바뀜)
    next_key = copy.deepcopy(ct)
    next_key[0] = 0
    return next_key

#============================================
# Encryption chain 만들기
# 입력:
#   시작점 : SP (24bit 랜덤키)
#   고정평문 : P0 (32bit)
#   길이 : t (체인의 길이 t = 2^8 = (2^24)^(1/3))
# 출력:
#   끝점 : EP
def chain_EP(SP, P0, t):
    Xj = SP
    for j in range(0, t):
        ct = TC20_Enc_lib.TC20_Enc(P0, Xj)
        Xj = R(ct) # X_{j+1}
    return Xj

'''
# Chain 출력하고 싶을 경우
def chain_EP_print(SP, P0, t):
    Xj = SP
    print('SP = ', SP)
    for j in range(0, t):
        ct = TC20_Enc_lib.TC20_Enc(P0, Xj)
        Xj = R(ct) # X_{j+1}
        print('--> ', ct, ' -->', Xj)
    return Xj

# chain 퍄일 만들고 싶을 경우
def chain_EP_file(SP, P0, t, chain_num, table_num):
    file_name = 'TMTO/TMTO-chain-' + str(table_num) + '-' + str(chain_num) + '.txt'
    f = open(file_name, 'w+')
    Xj = SP
    #print('SP = ', SP)
    f.write('SP = [0, %d, %d, %d]\n' %(Xj[1], Xj[2], Xj[3]))
    for j in range(0, t):
        ct = TC20_Enc_lib.TC20_Enc(P0, Xj)
        Xj = R(ct) # X_{j+1}
        f.write('--> [%d, %d, %d, %d] ' %(ct[0], ct[1], ct[2], ct[3]))
        f.write('--> [%d, %d, %d, %d]\n' %(Xj[0], Xj[1], Xj[2], Xj[3]))
    f.close()
    return Xj
'''

#====================================
# TMTO 테이블 한개 만들기
# 입력 :
#   P0 : 고정평문 
#   m : 행(row)의 개수 (체인의 개수)
#   t : 열(col)의 개수 (체인의 길이)
#   ell : 테이블 번호 (TMTO 테이블 번호 : 0, 1, 2, ..., 255)
def make_one_tmto_table(P0, m, t, ell):
    tmto_dic = {}  # = {(SP0, EP0), (SP1, EP1) ... (SP_{m-1}, EP_{m-1})}
    for i in range(0, m):
        SP = [0, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        EP = chain_EP(SP, P0, t)
        SP_int = int_list_lib.list2int(SP)
        EP_int = int_list_lib.list2int(EP)
        tmto_dic[EP_int] = SP_int
    file_name = 'TMTO_Tables/TMTO-' + str(ell) + '.dic'
    pickle_file.save_var_to_file(tmto_dic, file_name)

#====================================
# TMTO 테이블 전체 만들기
# 입력 :
#   P0 : 고정평문 
#   m : 행(row)의 개수 (체인의 개수)
#   t : 열(col)의 개수 (체인의 길이)
#   num_of_tables : TMTO 테이블 개수 (=256)
def make_all_tmto_tables(P0, m, t, num_of_tables):
    print('making TMTO tables', end='')
    for ell in range(0, num_of_tables):
        make_one_tmto_table(P0, m, t, ell)
        print('.', end='')
    print('\n %d TMTO tables are created.\n' %(num_of_tables))

#===============================
# 한개의 테이블을 읽고 후보 암호키를 리스트에 넣는다.
# 입력:
#   ct = E(P0, unknown_key)
#   m : 행(row)의 개수 (체인의 개수)
#   t : 열(col)의 개수 (체인의 길이)
#   ell : 테이블 번호 (TMTO 테이블 번호 : 0, 1, 2, ..., 255)
def one_tmto_table_search(ct, P0, m, t, ell):
    key_candid_list = []
    file_name = 'TMTO_Tables/TMTO-' + str(ell) + '.dic'
    tmto_dic = pickle_file.load_var_from_file(file_name)

    Xj = R(ct)
    current_j = t
    for idx in range(0, t):
        Xj_int = int_list_lib.list2int(Xj)

        if Xj_int in tmto_dic: #Xj가 EP중에 있는지?
            SP = int_list_lib.int2list(tmto_dic[Xj_int]) # EP --> SP
            key_guess = chain_EP(SP, P0, current_j-1)
            key_candid_list.append(key_guess)
        new_ct = TC20_Enc_lib.TC20_Enc(P0, Xj)
        Xj = R(new_ct)
        current_j = current_j - 1
    
    return key_candid_list


#===========================================
# (0) 실행
#=======================================
random.seed(1234) # 고정된 seed 사용 (고정되지 않은 seed 사용법은?)
P0 = [1, 2, 3, 4]

m = 256  # 행(row)의 개수 (체인의 개수)
t = 256  # 열(col)의 개수 (체인의 길이)
tables = 256 # 테이블 개수

#======================
# (1)TMTO 테이블 만들기
#======================
make_all_tmto_tables(P0, m, t, tables)

#========================
# (2) TMTO 공격 알고리즘
#========================
ct1 = TC20_Enc_lib.TC20_Enc(P0, [0, 20, 90, 139]) # ct1 = [100, 107, 220, 57]
key_pool = []

print('Pt1 =', P0)
print('ct1 =', ct1)

print('\nTMTO Attack', end='')
for ell in range(0, tables):
    key_list = one_tmto_table_search(ct1, P0, m, t, ell)
    key_pool += key_list
    print('.', end='')
print('\n Attack complete!\n')
print('guess key list :', key_pool)

pt2 = [5, 6, 7, 8]
ct2 = TC20_Enc_lib.TC20_Enc(pt2, [0, 20, 90, 139]) # ct2 = [72, 215, 32, 51]
final_key = []

print('\nPt2 =', P0)
print('ct2 =', ct1)

for key in key_pool:
    ct_result = TC20_Enc_lib.TC20_Enc(pt2, key)
    if ct_result == ct2:
        final_key.append(key)
print('\nFinal_key = ', end='')
print(final_key)