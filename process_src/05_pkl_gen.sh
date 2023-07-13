
# 生成pkl（去前2帧），用于生成via标注	      （yolov5_det/labels -- dense_proposals_train.pkl）
python ./process_src/dense_proposals_train.py ./process_file/yolov5_det/labels ./process_file/dense_proposals_train.pkl show

# 准备deepsort完整pkl，用于跟踪检测人ID	  （detect/labels -- dense_proposals_train_deepsort.pkl）
python ./process_src/dense_proposals_train_deepsort.py ./process_file/yolov5_det/labels ./process_file/dense_proposals_train_deepsort.pkl show