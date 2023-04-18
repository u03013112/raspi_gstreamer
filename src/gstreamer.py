import cv2
import numpy as np
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

def stitch_frames(frame1, frame2):
    # 在这里实现你的拼接算法
    stitched_frame = np.concatenate((frame1, frame2), axis=1)
    return stitched_frame

def main():
    Gst.init(None)

    cap1 = cv2.VideoCapture(0)
    cap2 = cv2.VideoCapture(1)

    pipeline = Gst.parse_launch("appsrc ! videoconvert ! x264enc ! rtph264pay ! udpsink host=127.0.0.1 port=5000")
    appsrc = pipeline.get_by_name("appsrc0")
    pipeline.set_state(Gst.State.PLAYING)

    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if not ret1 or not ret2:
            break

        stitched_frame = stitch_frames(frame1, frame2)
        _, data = cv2.imencode('.jpg', stitched_frame)
        buf = Gst.Buffer.new_wrapped(data.tobytes())
        appsrc.emit("push-buffer", buf)

    pipeline.set_state(Gst.State.NULL)
    cap1.release()
    cap2.release()

if __name__ == "__main__":
    main()