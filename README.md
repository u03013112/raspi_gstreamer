# raspi_gstreamer
树莓派 usb 摄像头 视频流

第一步，读取2个USB摄像头图片，然后进行简单拼接，然后进行编码，然后进行推流。
封装成一个docker镜像，然后在树莓派上运行。
尽可能的减少时延和CPU使用。

## 简单的视频通讯
树莓派上（server）cmd
gst-launch-1.0 -v v4l2src device=/dev/video0 ! video/x-raw,width=640,height=480,framerate=15/1 ! videoconvert ! jpegenc ! rtpjpegpay ! udpsink host=192.168.1.101 port=5000 sync=false
macos（client）cmd
gst-launch-1.0 -v udpsrc port=5000 ! application/x-rtp,media=video,payload=26,clock-rate=90000,encoding-name=JPEG ! rtpjpegdepay ! jpegdec ! autovideosink
