import os
import cv2
import glob

# 현재 파일 기준으로 CCTV 폴더 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, 'cctv')

# jpg 파일 목록 불러오기 (정렬)
images = sorted(glob.glob(os.path.join(IMG_DIR, '*.jpg')))

if not images:
    raise FileNotFoundError(f"cctv 폴더에 jpg 이미지가 없습니다: {IMG_DIR}")

index = 0  # 현재 보여줄 이미지 인덱스

while True:
    img_path = images[index]
    img = cv2.imread(img_path)

    if img is None:
        print(f"이미지를 읽을 수 없습니다: {img_path}")
        break

    if img is not None:
        print('조작방법 : 방향키(왼쪽/오른쪽) 또는 a/d 키로 이미지 전환, ESC로 종료')

    # 파일명 표시
    cv2.imshow("CCTV Viewer", img)
    print(f"현재 이미지: {os.path.basename(img_path)} ({index+1}/{len(images)})")

    key = cv2.waitKey(0) & 0xFF  # 키 입력 대기

    if key == 27:  # ESC → 종료
        break
    elif key == 83 or key == ord('d'):  # 오른쪽 방향키(Windows: 83), 또는 'd'
        index = (index + 1) % len(images)  # 다음 이미지
    elif key == 81 or key == ord('a'):  # 왼쪽 방향키(Windows: 81), 또는 'a'
        index = (index - 1) % len(images)  # 이전 이미지

cv2.destroyAllWindows()
