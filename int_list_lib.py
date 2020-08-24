#--------------------------
# 정수 -> 리스트로
# 예) 0x12345678 --> [0x12, 0x34, 0x56, 0x78] 0x:16진수
def int2list(n):
    out_list = []
    out_list.append((n >> 24) & 0x000000ff)  #0x00000012 = (0x12345678 >> 24)
    out_list.append((n >> 16) & 0xff)  #0x00001234 = (0x12345678 >> 16)
    out_list.append((n >> 8) & 0xff)  #0x00123456 = (0x12345678 >> 8)
    out_list.append(n & 0xff)  #0x12345678

    return out_list

#-------------------------
# 리스트 -> 정수로
def list2int(lst):
    n = 0
    num_bytes = len(lst)  #num_bytes = 4
    for i in range(num_bytes):  # i = 0, 1, 2, 3
        n += lst[i] << 8*(num_bytes - 1 - i) 
        # i=0 : << 8*(4-1-0) = <<24 
        # i=1 : << 8*(4-1-1) = <<16
    return n
