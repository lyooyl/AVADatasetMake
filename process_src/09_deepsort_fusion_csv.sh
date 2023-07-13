
# deepsort检测人ID	（frames & dense_proposals_train_deepsort.pkl -- train_personID.csv）
echo "开始deepsort人物ID的跟踪检测"
python ./process_src/yolovDeepsort/yolov5_to_deepsort.py
echo "ok. 完成人物ID检测"

# 融合人ID&action		（train_personID.csv && train_without_personID.csv -- train_temp.csv）
python ./process_src/train_temp.py

# 修正csv的-1值		（train_temp.csv -- ./annotations/train.csv）
python ./process_src/train.py
echo "ok. 融合CSV结果文件已生成到./ava_finally/annotations/train.csv"

touch ava_finally/annotations/train_excluded_timestamps.csv
echo "    补充：创建ava_finally/annotations/train_excluded_timestamps.csv (默认为空)"