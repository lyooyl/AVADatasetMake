
# rawframes生成（拷贝）		（frames -- rawframes）
echo "./process_file/frames/*  -->  ./ava_finally/rawframes"
echo "开始复制..."
if [ ! -d "ava_finally/rawframes" ]; then
  echo "路径不存在，正在创建..."
  # 创建路径
  mkdir -p "ava_finally/rawframes"
fi
cp -r process_file/frames/*  ava_finally/rawframes
echo "复制完成！"


# 改名 --> prefix=='img_'
echo "开始规范命名..."
python process_src/change_raw_frames.py
echo "原帧制作完成！"


