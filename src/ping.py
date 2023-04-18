# 在发送端，将当前时间戳绘制到视频帧上：
# python
import cv2
import time

# ... 其他代码，如读取摄像头帧 ...

# 在帧上绘制当前时间戳
timestamp = int(time.time() * 1000)  # 毫秒为单位
text = f"Timestamp: {timestamp}"
cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# ... 将帧编码为JPEG并发送到GStreamer管道 ...
# 在接收端，从视频帧中读取时间戳，并计算时延：
# python
import cv2
import time
import re

# ... 其他代码，如从GStreamer管道接收视频帧 ...

# 从帧中提取时间戳
text_roi = frame[0:40, 0:500]
gray = cv2.cvtColor(text_roi, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
ocr_result = pytesseract.image_to_string(binary, config="--psm 6")
timestamp_match = re.search(r"Timestamp: (\d+)", ocr_result)

if timestamp_match:
    timestamp = int(timestamp_match.group(1))

    # 计算时延
    current_time = int(time.time() * 1000)  # 毫秒为单位
    delay = current_time - timestamp
    print("Delay:", delay, "ms")
请注意，这个示例使用了pytesseract库来识别视频帧中的时间戳文本。你需要先安装Tesseract OCR引擎和pytesseract库：

bash
# 安装Tesseract OCR引擎（以Ubuntu为例）
sudo apt-get install tesseract-ocr

# 安装pytesseract库
pip install pytesseract
这种方法的准确性取决于发送端和接收端的时钟同步程度。你可以使用NTP或PTP等协议来同步时钟。此外，如果文本识别结果不理想，可以尝试调整二值化阈值或使用其他OCR库。




要在客户端测量图像时延，你可以在发送端和接收端都添加时间戳。以下是一个简单的方法，使用Python和GStreamer在发送端和接收端分别添加和读取时间戳：

在发送端，将当前时间戳添加到每个Gst.Buffer的元数据中：

python
import time

# ... 其他代码 ...

while True:
    # ... 从摄像头读取和拼接帧的代码 ...

    _, data = cv2.imencode('.jpg', stitched_frame)
    buf = Gst.Buffer.new_wrapped(data.tobytes())

    # 添加当前时间戳到Gst.Buffer的元数据
    timestamp = int(time.time() * 1000)  # 毫秒为单位
    buf.pts = timestamp

    appsrc.emit("push-buffer", buf)
在接收端，从接收到的Gst.Buffer中读取时间戳，并计算时延：

python
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

def on_new_sample(sink):
    sample = sink.emit("pull-sample")
    buf = sample.get_buffer()

    # 从Gst.Buffer的元数据中读取时间戳
    timestamp = buf.pts

    # 计算时延
    current_time = int(time.time() * 1000)  # 毫秒为单位
    delay = current_time - timestamp
    print("Delay:", delay, "ms")

    return Gst.FlowReturn.OK

# ... 创建GStreamer管道和接收视频流的代码 ...

# 将回调函数连接到接收端的"sink"元素
sink = pipeline.get_by_name("sink_name")  # 请根据实际情况替换为sink元素的名称
sink.connect("new-sample", on_new_sample)

# ... 启动GStreamer管道和主循环的代码 ...
请注意，这个示例假设你在接收端使用Python和GStreamer。如果你使用的是其他客户端（如VLC或GStreamer命令行工具），则需要根据具体情况修改代码以读取和计算时间戳。

此外，这个示例仅计算了图像在发送端和接收端之间的时延。实际应用中，可能还需要考虑其他因素（如网络延迟、解码时间等），以获得更准确的时延估计。