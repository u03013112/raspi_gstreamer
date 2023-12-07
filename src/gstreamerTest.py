import cv2

build_info = cv2.getBuildInformation()
gstreamer_enabled = "GStreamer" in build_info

print("GStreamer support:", gstreamer_enabled)