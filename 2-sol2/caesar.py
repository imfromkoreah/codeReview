def caesar_cipher_decode(target_text):
    # 결과 리스트
    decoded_texts = []
    
    # 알파벳 개수 (26글자)
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    
    # 1부터 26까지 자리수만큼 암호를 풀어본다
    for shift in range(1, 27):
        decoded_text = ''
        
        for char in target_text:
            if char.isalpha():  # 알파벳인 경우만 처리
                # 소문자일 경우
                if char.islower():
                    new_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                # 대문자일 경우
                elif char.isupper():
                    new_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                decoded_text += new_char
            else:
                decoded_text += char  # 알파벳이 아닌 문자들은 그대로 추가
                
        decoded_texts.append((shift, decoded_text))  # 자리수와 함께 저장
    
    # 결과 출력
    for shift, decoded_text in decoded_texts:
        print(f'자리수 {shift}: {decoded_text}')
    
    # 사용자가 직접 눈으로 식별하고 결과를 반환
    correct_shift = int(input("암호가 풀린 자리수를 입력하세요: "))
    
    # 풀린 결과를 result.txt에 저장
    with open('C:/Users/xxivo/Desktop/codyssey/2-sol1/result.txt', 'w') as result_file:
        result_file.write(decoded_texts[correct_shift - 1][1])
    
    print('결과가 result.txt에 저장되었습니다.')

# 암호 텍스트를 파일에서 읽어오기
try:
    # password.txt 파일 경로 수정 (2-sol1 폴더에서 읽어오기)
    with open('C:/Users/xxivo/Desktop/codyssey/2-sol1/password.txt', 'r') as file:
        target_text = file.read()
    
    # 카이사르 암호 해독 수행
    caesar_cipher_decode(target_text)
except FileNotFoundError:
    print('2-sol1/password.txt 파일을 찾을 수 없습니다.')
