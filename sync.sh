#!/bin/bash
# mac上运行的脚本，用于同步本地文件到服务器上
# 检测到本地文件有变化后，自动同步到服务器上
SRCDIR=~/Documents/git/raspi_gstreamer
DST=root@raspi.local:/home/git/

# 安装fswatch
if ! command -v fswatch &> /dev/null
then
    echo "fswatch未安装，请先使用brew install fswatch进行安装"
    exit
fi

# 本地文件有变化后，自动同步到服务器上
fswatch -o -r --exclude=".*\.swp" "$SRCDIR" | while read f
do
    rsync -avz --delete --exclude=".*" "$SRCDIR" "$DST"
    say 红鲤鱼与绿鲤鱼与驴
done