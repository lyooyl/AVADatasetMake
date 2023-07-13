
/home/lyo/miniconda3/envs/py38/bin/python ./process_src/yolovDeepsort/yolov5/detect.py \
--weights ./process_src/yolovDeepsort/yolov5/yolov5s.pt \
--source ./process_file/choose_frames_all/ \
--classes 0 \
--save-txt \
--save-conf \
--project ./process_file \
--name yolov5_det
