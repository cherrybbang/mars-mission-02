import zipfile
import itertools
import string
import time
from datetime import datetime

# zip 파일 경로
zip_file_path = 'emergency_storage_key.zip'

characters = string.ascii_lowercase + string.digits
min_length = 6
max_length = 6

def unlock_zip(zip_file, password):
    try:
        zip_file.extractall(pwd=password.encode('utf-8'))
        print(f'비밀번호를 찾았습니다! : {password}')
        
        # 비밀번호를 password.txt 파일에 저장
        with open('password.txt', 'w') as f:
            f.write(password)
        print(f'비밀번호가 password.txt 파일에 저장되었습니다.')
        
        return True
    except:
        return False
start_time = time.time()
start_datetime = datetime.now()
print(f'시작 시간: {start_datetime.strftime("%Y-%m-%d %H:%M:%S")}')
    
with zipfile.ZipFile(zip_file_path) as zf:
    found = False
    attempt_count = 0

    for length in range(min_length, max_length + 1):
        for attempt in itertools.product(characters, repeat=length):
            attempt_count += 1
            password = ''.join(attempt)

            if unlock_zip(zf, password):
                found = True
                break
        if found:
            break
        
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    if found:
        print(f'총 시도 횟수: {attempt_count}회')
        print(f'걸린 시간: {elapsed_time:.2f}초')
        print(f'종료 시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    else:
        print('비밀번호를 찾지 못했습니다ㅠㅠ')