# 单摄像头版本，用于测试
import cv2
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

def main():
    Gst.init(None)

    cap = cv2.VideoCapture(0)

    # omxh264enc是一个硬件加速的H.264编码器，通常在具有OpenMAX支持的设备（如树莓派）上使用。
    # pipeline = Gst.parse_launch("appsrc ! videoconvert ! omxh264enc target-bitrate=1000000 control-rate=1 ! video/x-h264,profile=baseline ! h264parse ! rtph264pay config-interval=1 ! udpsink host=127.0.0.1 port=5000")
    pipeline = Gst.parse_launch("appsrc ! videoconvert ! x264enc bitrate=1000 ! video/x-h264,profile=baseline ! h264parse ! rtph264pay config-interval=1 ! udpsink host=127.0.0.1 port=5000")
    appsrc = pipeline.get_by_name("appsrc0")
    pipeline.set_state(Gst.State.PLAYING)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # 将图像编码为JPEG并发送到GStreamer管道
        _, data = cv2.imencode('.jpg', frame)
        buf = Gst.Buffer.new_wrapped(data.tobytes())
        appsrc.emit("push-buffer", buf)

    pipeline.set_state(Gst.State.NULL)
    cap.release()

if __name__ == "__main__":
    main()