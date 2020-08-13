# Toy-Cipher
- TC20 암호화 라이브러리 구현
- TC20 복호화 라이브러리 구현
- TC20 암호화 복호화 실행 코드 구현
- TC20 Brute Force Attack 구현
- TC20 MITM 구현

## TC20 구조
### TC20 블록암호
- 블록 크기 : 32bit
- 키 크기 : 32bit
- 라운드 수 : 10
- 구조 : SPN (Substitution Permutation Network)

### TC20 - Add Roundkey (라운드키 적용)
- 라운드키 : RK = (rk0, rk1, rk2, rk3)
- (y0, y1, y2, y3) = (x0 ^ rk0, x1 ^ rk1, x2 ^ rk2, x3 ^ rk3)

<img src="https://user-images.githubusercontent.com/68969252/90105144-63509800-dd80-11ea-8da8-37a1af5712cd.PNG" width="430">

### TC20 - Sbox (비선형 변환)
- AES와 동일한 Sbox 사용 (8bit -> 8bit)
- 각 라운드마다 4개의 Sbox를 각 바이트에 적용

<img src="https://user-images.githubusercontent.com/68969252/90105308-a3b01600-dd80-11ea-8322-f10c5effbb83.PNG" width = "300">

### TC20 - Linear Map (선형 변환)
- 4바이트에 대한 바이트 단위의 선형변환
- 4 x 4 이진(binary) 행렬 A로 표현되는 함수 : Y = AX

<img src="https://user-images.githubusercontent.com/68969252/90105999-c131af80-dd81-11ea-8e2e-244f02ea5be6.PNG" width="300">

<img src="https://user-images.githubusercontent.com/68969252/90105838-86c81280-dd81-11ea-834a-77d0828f44db.PNG" width="330">

## TC20 공격
- Brute Force Attack : Exhaustive key search (암호키 전수조사)
- Meet-in-the-Middle Attack

## TC20 실행화면
### TC20_Enc_lib.py 실행화면
<img src="https://user-images.githubusercontent.com/68969252/90107827-62ba0080-dd84-11ea-8a34-2af8cef81a1b.PNG" width="300">

### TC20_Dec_lib.py 실행화면
<img src="https://user-images.githubusercontent.com/68969252/90107681-24244600-dd84-11ea-808f-26f05685657c.PNG" width="300">

### Run_TC20.py 실행화면
![tc9](https://user-images.githubusercontent.com/68969252/90109921-6ef38d00-dd87-11ea-921b-06cb935a7118.PNG)
