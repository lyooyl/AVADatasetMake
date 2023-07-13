IN_DATA_DIR="./process_file/videos"
OUT_DATA_DIR="./process_file/videos_crop"
# 判断路径是否存在
if [ ! -d "${OUT_DATA_DIR}" ]; then
  echo "路径不存在，正在创建..."
  # 创建路径
  mkdir -p "${OUT_DATA_DIR}"
fi

ffmpeg -i ${IN_DATA_DIR}/drink_22.mp4 -r 30 -ss 0 -t 11 ${OUT_DATA_DIR}/22.mp4 -y 
ffmpeg -i ${IN_DATA_DIR}/drink_49.mp4 -r 30 -vf "setpts=(PTS-STARTPTS)*(11/10)" -c:a copy ${OUT_DATA_DIR}/49.mp4

