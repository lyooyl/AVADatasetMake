IN_DATA_DIR="./process_file/videos"
OUT_DATA_DIR="./process_file/videos_crop"
# 判断路径是否存在
if [ ! -d "${OUT_DATA_DIR}" ]; then
  echo "路径不存在，正在创建..."
  # 创建路径
  mkdir -p "${OUT_DATA_DIR}"
fi
# 设置要获取文件名的目录路径
files=$(ls ${IN_DATA_DIR})
# 循环遍历
idx=0
for file in $files
do
    echo "正在处理${file}"
    # NEW_NAME=$(cut -d'_' -f2 <<< ${file})
    NEW_NAME=$(printf "%02d" $idx).mp4
    LEN_TIME=$(ffprobe -i ${IN_DATA_DIR}/${file} -show_entries format=duration -v quiet -of csv="p=0")
    k=11.0/$LEN_TIME
    ffmpeg -i ${IN_DATA_DIR}/${file} -vf "setpts=PTS*$k" -r 30 -ss 0 -t 11 ${OUT_DATA_DIR}/${NEW_NAME} -y
    # if [ $(echo "$LEN_TIME < 11.0" | bc) -eq 1 ]; then
    #   echo "时长小于11秒"
    #   ffmpeg -i ${IN_DATA_DIR}/${file} -vf "setpts=PTS*$k" -r 30 -ss 0 -t 11 ${OUT_DATA_DIR}/${NEW_NAME} -y
    # else
    #   ffmpeg -i ${IN_DATA_DIR}/${file} -r 30 -ss 0 -t 11 ${OUT_DATA_DIR}/${NEW_NAME} -y
    # fi
    idx=$((idx + 1))
done



