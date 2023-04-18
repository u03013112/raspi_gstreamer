import cv2
import gi
import numpy as np
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

def gst_to_opencv(sample):
    buf = sample.get_buffer()
    caps = sample.get_caps()
    width = caps.get_structure(0).get_value("width")
    height = caps.get_structure(0).get_value("height")

    buf_data = buf.extract_dup(0, buf.get_size())
    img_array = np.ndarray((height, width, 3), buffer=buf_data, dtype=np.uint8)
    return img_array

def new_sample(sink, data):
    sample = sink.emit("pull-sample")
    frame = gst_to_opencv(sample)
    cv2.imshow("Video", frame)
    cv2.waitKey(1)
    return Gst.FlowReturn.OK

def main():
    Gst.init(None)

    pipeline_str = "udpsrc port=5000 ! application/x-rtp,encoding-name=H264,payload=96 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink"
    pipeline = Gst.parse_launch(pipeline_str)

    appsink = pipeline.get_by_name("appsink0")
    appsink.connect("new-sample", new_sample, None)

    pipeline.set_state(Gst.State.PLAYING)
    cv2.namedWindow("Video", cv2.WINDOW_AUTOSIZE)

    try:
        GLib.MainLoop().run()
    except KeyboardInterrupt:
        pass

    pipeline.set_state(Gst.State.NULL)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print('start')
    main()