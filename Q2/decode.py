import string

# 비밀번호 파일 읽기
with open('../Q1/password.txt', 'r') as f:
    encrypted_text = f.read().strip()

# 2. 복호화 함수
def caesar_cipher_decode(target_text):
    alphabet = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
    for shift in range(1, 26):  # 1~25
        decoded = ''
        for char in target_text:
            if char.islower():
                idx = (alphabet.index(char) - shift) % 26
                decoded += alphabet[idx]
            elif char.isupper():
                idx = (alphabet.index(char.lower()) - shift) % 26
                decoded += alphabet[idx].upper()
            else:
                decoded += char  # 숫자, 공백, 특수문자 등은 그대로
        print(f"[{shift:2d}] {decoded}")

# 3. 복호화 시도
print("\n가능한 복호화 결과들 (1~25 자리 이동):\n")
caesar_cipher_decode(encrypted_text)

# 4. 사용자에게 번호 입력 받기
try:
    choice = int(input("\n몇 번째 자리수로 해독된 것 같나요? (1~25 사이 숫자 입력): "))
    if not (1 <= choice <= 25):
        raise ValueError("1~25 범위 숫자 아님")

    # 다시 해당 shift로 정확한 결과 구해서 저장
    def decode_with_shift(text, shift):
        result = ''
        for char in text:
            if char.islower():
                result += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            elif char.isupper():
                result += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                result += char
        return result

    result = decode_with_shift(encrypted_text, choice)

    with open('result.txt', 'w', encoding='utf-8') as f:
        f.write(result)

    print(f"\n결과가 result.txt에 저장되었습니다! (자리수: {choice})")

except ValueError as e:
    print(f"\n잘못된 입력입니다: {e}")
