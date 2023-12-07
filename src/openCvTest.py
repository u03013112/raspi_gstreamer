import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if ret:
        # 处理帧的代码（如果需要）可以放在这里
        print('.')
        pass
    else:
        break

cap.release()