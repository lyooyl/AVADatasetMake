
# 初始导出via标注 （dense_proposals_train.pkl & choose_frames_middle -- choose_frames_middle/_proposal.json）
python ./process_src/dense_proposals_train_to_via.py ./process_file/dense_proposals_train.pkl ./process_file/choose_frames_middle/
echo "ok. 第一次导出via n_proposal.json"

# 去除via默认值		（choose_frames_middle/_proposal.json -- _proposal_s.json）
python ./process_src/changs_via_json.py ./process_file/choose_frames_middle
echo "ok. 第二次导出via n_proposal_s.json"


# 生成最终pkl标注
echo " ======== 开始生成最终pkl标注 ========"
OUT_PKL_DIR="./ava_finally/annotations"
if [ ! -d "${OUT_PKL_DIR}" ]; then
  echo "路径不存在，正在创建..."
  mkdir -p "${OUT_PKL_DIR}"
fi
# 复制、修正dense_proposals_train.pkl超限值[0,1]  （dense_proposals_train.pkl覆盖）
cp ./process_file/dense_proposals_train.pkl ${OUT_PKL_DIR}
python ./process_src/change_dense_proposals_train.py ${OUT_PKL_DIR}/dense_proposals_train.pkl
echo "ok.   生成最终dense_proposals_train.pkl标注 --> ava_finally/annotations/"


echo "    现在，请打开via软件，在'./process_file/choose_frames_middle'下标注所有clip。"
echo "        viaImage: x/*.jpg       viaJson: x/x_proposal_s.json"
echo "    标注完成后，另存json到: x/x_finish.json"
## via标注action		（choose_frames_middle/_proposal_s.json -- _finish.json）
#  # 软件标注行为




