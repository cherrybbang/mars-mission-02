import random
import zipfile
import time

start_time = time.time()
attempt_count = 0

while True:
  set = 'abcdefghijklmnopqrstuvwxyz0123456789'
  zfile = zipfile.ZipFile('emergency_storage_key.zip', 'r')
  paw = ''

  for i in range(0,6):
    paw += random.choice(set)

    attempt_count += 1
    print(f"시도 #{attempt_count}: {paw} 테스트 중...")

    if zfile:
      try:
        zfile.extractall(path='.', pwd=str(paw).encode('utf-8'))
        end_time = time.time()
        print(f'비밀번호는 {paw} 입니다!')
        print(f'시작시간 : {start_time}')
        print(f'소요시간 : {end_time - start_time}')

        with open('password.txt', 'w', encoding='utf-8') as f:
            f.write(f'비밀번호: {paw}\n')

        print('비밀번호가 password.txt 파일에 저장되었습니다.')
        break
      
      except:
        pass