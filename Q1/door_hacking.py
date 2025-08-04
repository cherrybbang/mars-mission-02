import zipfile
import itertools
import string

# zip 파일 경로
zip_file_path = 'Q1/emergency_storage_key.zip'

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
    
with zipfile.ZipFile(zip_file_path) as zf:
    found = False
    for length in range(min_length, max_length + 1):
        for attempt in itertools.product(characters, repeat=length):
            password = ''.join(attempt)
            print(f'시도 중인 숫자 : {password}')
            if unlock_zip(zf, password):
                found = True
                break
        if found:
            break
    
    else:
        print('비밀번호를 찾지 못했습니다ㅠㅠ')