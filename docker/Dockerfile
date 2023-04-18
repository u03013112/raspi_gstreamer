FROM python:3.7-slim-buster

RUN apt-get update && apt-get install -y \
    libgstreamer1.0-0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    gstreamer1.0-doc \
    gstreamer1.0-tools \
    libgirepository1.0-dev \
    libcairo2-dev \
    libgstreamer-plugins-base1.0-dev \
    libraspberrypi0 \
    libopencv-dev \
    python3-opencv \
    python3-gst-1.0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
WORKDIR /app
RUN pip3 install -r requirements.txt

COPY . /app

CMD ["python3", "main.py"]