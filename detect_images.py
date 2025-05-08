#!/usr/bin/env python3
from ultralytics import YOLO
import cv2, glob, os

# 모델 가중치 파일 경로
WEIGHTS = '/Users/shin/capstone/ultralytics/yolov8s_babyfinder_continue4/weights/best.pt'

# 입력 이미지 디렉토리와 확장자 (jpg, png 등)
IMAGE_DIR = '/Users/shin/capstone/ultralytics/images'
IMAGE_EXT = 'jpg'  # 필요에 따라 'png' 등으로 변경

# 결과를 저장할 디렉토리
SAVE_DIR = '/Users/shin/capstone/ultralytics/output'
os.makedirs(SAVE_DIR, exist_ok=True)

# YOLOv8 모델 로드
model = YOLO(WEIGHTS)

def main():
    img_paths = glob.glob(os.path.join(IMAGE_DIR, f'*.{IMAGE_EXT}'))
    if not img_paths:
        print(f'No images found in {IMAGE_DIR} with extension {IMAGE_EXT}')
        return

    for p in img_paths:
        img = cv2.imread(p)
        if img is None:
            print(f'Failed to load {p}')
            continue

        # 예측 수행 (필요시 conf, imgsz 등 파라미터 추가 가능)
        results = model(img)
        # 결과 시각화
        annotated = results[0].plot()

        # 파일명 그대로 저장
        out_path = os.path.join(SAVE_DIR, os.path.basename(p))
        cv2.imwrite(out_path, annotated)
        print(f'[saved] {out_path}')

if __name__ == '__main__':
    main() 