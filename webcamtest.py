from ultralytics import YOLO
import cv2

# 모델 로드
model = YOLO('/Users/shin/capstone/ultralytics/yolov8s_babyfinder_continue4/weights/best.pt')

# 웹캠 열기
# cap = cv2.VideoCapture(0)
# 아이폰으로 
cap = cv2.VideoCapture(1)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # YOLO 모델로 프레임 탐지
    results = model(frame)

    # 탐지 결과를 시각화
    annotated_frame = results[0].plot()

    # OpenCV 창으로 띄우기
    cv2.imshow('YOLOv8 Webcam Detection', annotated_frame)

    # 'q' 키 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()