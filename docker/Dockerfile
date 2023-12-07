# 使用官方树莓派4的Python镜像作为基础镜像
FROM balenalib/raspberrypi4-64-python:buster

# 安装必要的依赖项
RUN apt-get update && apt-get install -y \
    python3-opencv \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-omx \
    libgstreamer1.0-dev \
    libgstrtspserver-1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装libcairo2-dev和pkg-config
RUN apt-get update && apt-get install -y \
    libcairo2-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 安装与gcc相关的依赖项
RUN apt-get update && apt-get install -y \
    libcairo2-dev \
    pkg-config \
    gcc \
    g++ \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# 使用国内源加速pip
RUN mkdir -p /root/.pip \
    && echo '[global]' > /root/.pip/pip.conf \
    && echo 'index-url = https://pypi.tuna.tsinghua.edu.cn/simple' >> /root/.pip/pip.conf

RUN apt-get update && apt-get install -y libgirepository1.0-dev

COPY requirements.txt /requirements.txt
WORKDIR /src
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt