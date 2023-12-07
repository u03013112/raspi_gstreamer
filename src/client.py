import gi
import numpy as np
import cv2
import os
import time

gi.require_version("Gst", "1.0")
gi.require_version("GstApp", "1.0")
from gi.repository import Gst

Gst.init(None)

def on_new_sample(sink, pipeline, app):
    sample = sink.emit("pull-sample")
    buffer = sample.get_buffer()
    caps = sample.get_caps()
    width = caps.get_structure(0).get_value("width")
    height = caps.get_structure(0).get_value("height")

    success, mapinfo = buffer.map(Gst.MapFlags.READ)
    if success:
        frame = np.ndarray((height, width, 3), buffer=mapinfo.data, dtype=np.uint8)
        if pipeline == pipeline1:
            app.frame1 = frame.copy()
        elif pipeline == pipeline2:
            app.frame2 = frame.copy()
        buffer.unmap(mapinfo)

    return Gst.FlowReturn.OK

def create_pipeline(port, app):
    pipeline = Gst.parse_launch(f"udpsrc port={port} ! application/x-rtp,media=video,payload=26,clock-rate=90000,encoding-name=JPEG ! rtpjpegdepay ! jpegdec ! videoconvert ! video/x-raw,format=BGR ! appsink name=sink emit-signals=True")
    sink = pipeline.get_by_name("sink")
    sink.connect("new-sample", on_new_sample, pipeline, app)
    return pipeline

class App:
    def __init__(self):
        self.frame1 = None
        self.frame2 = None

app = App()

pipeline1 = create_pipeline(5000, app)
pipeline2 = create_pipeline(5001, app)

pipeline1.set_state(Gst.State.PLAYING)
pipeline2.set_state(Gst.State.PLAYING)

while True:
    if app.frame1 is not None and app.frame2 is not None:
        combined_frame = np.hstack((app.frame1, app.frame2))
        cv2.imshow("Combined Video", combined_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("s"):
        timestamp = time.strftime("%y%m%d_%H%M%S", time.localtime())
        file_path = os.path.join("..", "pics", f"{timestamp}.jpg")
        cv2.imwrite(file_path, combined_frame)
        print(f"Screenshot saved to {file_path}")

pipeline1.set_state(Gst.State.NULL)
pipeline2.set_state(Gst.State.NULL)
cv2.destroyAllWindows()
