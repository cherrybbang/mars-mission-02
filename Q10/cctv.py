import os
import cv2
import glob

# Q9/cctv 폴더 경로 계산
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Q10 경로
Q9_DIR = os.path.join(BASE_DIR, '..', 'Q9')  # Q9 폴더
IMG_DIR = os.path.join(Q9_DIR, 'cctv')

# 이미지 확장자 필터
valid_ext = ('.jpg', '.jpeg', '.png', '.bmp')

# 이미지 목록 불러오기
images = sorted(
    [f for f in glob.glob(os.path.join(IMG_DIR, '*')) if f.lower().endswith(valid_ext)]
)

if not images:
    raise FileNotFoundError(f"이미지가 없습니다: {IMG_DIR}")

# HOG 기반 사람 감지기 초기화
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

index = 0
while index < len(images):
    img_path = images[index]
    img = cv2.imread(img_path)

    if img is None:
        print(f"이미지를 읽을 수 없습니다: {img_path}")
        index += 1
        continue

    # 사람 감지
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects, weights = hog.detectMultiScale(
        gray,
        winStride=(8, 8),
        padding=(16, 16),
        scale=1.05
    )

    if len(rects) > 0:
        # 사람 위치에 사각형 그리기
        for (x, y, w, h) in rects:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Detected Person", img)
        print(f"[사람 발견] {os.path.basename(img_path)}")
    else:
        print(f"[사람 없음] {os.path.basename(img_path)}")

    key = cv2.waitKey(0) & 0xFF
    if key == 27:  # ESC → 강제 종료
        break
    elif key == 13:  # 엔터 → 다음 이미지
        index += 1

cv2.destroyAllWindows()
print("검색이 끝났습니다.")
