import zipfile
import time
import itertools

def unlock_zip():
    # 암호를 풀 ZIP 파일 경로
    zip_file_path = 'C:/Users/xxivo/Desktop/codyssey/2-sol1/emergency_storage_key.zip'  # 파일 경로를 정확하게 설정
    # 파일을 저장할 경로
    password_file_path = 'C:/Users/xxivo/Desktop/codyssey/2-sol1/password.txt'
    
    # 가능한 모든 숫자 + 소문자 조합을 생성
    chars = '0123456789abcdefghijklmnopqrstuvwxyz'
    attempts = itertools.product(chars, repeat=6)
    
    # 시작 시간 기록
    start_time = time.time()
    attempt_count = 0

    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        # zip 파일의 암호가 맞을 때까지 시도
        for attempt in attempts:
            password = ''.join(attempt)  # 조합을 문자열로 변환
            attempt_count += 1
            try:
                # 암호를 시도해본다
                zip_file.setpassword(password.encode('utf-8'))
                zip_file.testzip()  # testzip()을 통해 암호가 맞는지 확인
                # 암호가 맞다면
                end_time = time.time()
                print(f'암호를 찾았습니다: {password}')
                print(f'시작 시간: {start_time}')
                print(f'반복 횟수: {attempt_count}')
                print(f'진행 시간: {end_time - start_time}초')

                # 암호를 파일에 저장
                with open(password_file_path, 'w') as password_file:
                    password_file.write(password)
                break
            except:
                # 암호가 틀린 경우에는 아무것도 하지 않음
                continue
        else:
            print("암호를 찾지 못했습니다.")

if __name__ == '__main__':
    unlock_zip()
