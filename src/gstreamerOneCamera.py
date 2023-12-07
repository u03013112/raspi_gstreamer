import cv2

def main():
    # 设置视频编码和发送流的GStreamer管道
    gst_out = "appsrc ! videoconvert ! x264enc bitrate=1000 ! video/x-h264,profile=baseline ! h264parse ! rtph264pay config-interval=1 ! udpsink host=127.0.0.1 port=5000"
    
    # 使用OpenCV的默认方法打开摄像头
    cap = cv2.VideoCapture(0)

    # 获取摄像头的帧大小
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (frame_width, frame_height)

    # 创建VideoWriter对象，使用GStreamer管道作为输出
    out = cv2.VideoWriter(gst_out, cv2.CAP_GSTREAMER, 0, 30, frame_size)

    # 检查VideoCapture和VideoWriter是否成功打开
    if not cap.isOpened():
        print("VideoCapture not opened")
        exit(0)
    if not out.isOpened():
        print("VideoWriter not opened")
        exit(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # 将捕获的帧写入GStreamer管道
            out.write(frame)

            # 显示捕获的帧（可选）
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # 释放资源
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()