# 【制作AVADataset数据集过程】
```
https://github.com/Whiffe/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset 
（1）代码执行在根目录./AVADatasetMake/下
（2）将输入视频文件放入./process_file/videos/下
```

## 01、电影剪辑片段
video -- videos_crop
- 修改sh脚本，使输出片段为11s、fps30、n.mp4命名
```shell
./process_src/01_cut_video.sh
```

## 02、按片段拆帧					
videos_crop -- frames(全部帧)
```shell
./process_src/02_cut_frames.sh 
```

## 03、缩减帧
frames -- choose_frames_all & choose_frames -- choose_frames_middle
- 检查sh中的python路径
```shell
./process_src/03_choose_frames.sh	
```

## 04、yolo检测
choose_frames_all -- yolov5_det
```shell
./process_src/04_yolo_det.sh
```

## 05、pkl生成
yolov5_det/labels -- dense_proposals_train.pkl & dense_proposals_train_deepsort.pkl
```shell
./process_src/05_pkl_gen.sh
```

## 06、via标注生成
dense_proposals_train.pkl & choose_frames_middle -- _proposal.json
- 修改./process_src/dense_proposals_train_to_via.py的第20行属性字典
```shell
./process_src/06_via_gen.sh	
```
	
## 07、via软件标注action
_proposal_s.json -- _finish.json
- 下载打开[VIA软件](https://www.robots.ox.ac.uk/~vgg/software/via/downloads/via3/via-3.0.11.zip )，进行行为标注...
- 打开*_proposal_s.json标注文件，标注行为信息，另存为*_finish.json

## 08、via转csv
_finish.json -- train_without_personID.csv
```shell
./process_src/08_via2csv.sh
```

## 09、deepsort检测跟踪，生成csv
frames & dense_proposals_train_deepsort.pkl & train_without_personID.csv -- train.csv
```shell
./process_src/09_deepsort_fusion_csv.sh
```

## 10、原帧生成
frames -- rawframes
```shell
./process_src/10_rawframes_gen.sh
```

## 11、其他文件创建

vim ./ava_finally/annotations/action_list.pbtxt # 写入行为列表，例中视频共两种行为，注意有缩进！
```text
item {
  name: "drink(left)"
  id: 1
}
  item {
  name: "drink(right)"
  id: 2
}
```

vim ./ava_finally/annotations/included_timestamps.txt  # 写入时间戳号，视频片段的middle为[02,08]共7帧(没用到)
```text
02
03
04
05
06
07
08
```
- val生成最与train相同。
## 最终，数据集结构如下
	├── data
	│   ├── ava
	│   │   ├── rawframes
	│   │   |   ├── 片段全帧图1/
	│   │   |   ├── 片段全帧图2/
	│   │   |   ├── ...
	│   │   ├── annotations
	│   │   |   ├── train.csv
	│   │   |   ├── [val.csv]
	│   │   |   ├── train_excluded_timestamps.csv
	│   │   |   ├── [val_excluded_timestamps.csv]	
	│   │   |   ├── dense_proposals_train.pkl
	│   │   |   ├── [dense_proposals_val.pkl]
	│   │   |   ├── action_list.pbtxt

 ## 数据集训练
 - 下载mmaction2
 ```shell
 git clone https://github.com/open-mmlab/mmaction2.git
```
- 修改[configs文件](https://github.com/open-mmlab/mmaction2/blob/main/configs/detection/slowfast/slowfast_kinetics400-pretrained-r50_8xb6-8x8x1-cosine-10e_ava22-rgb-drink-0725.py)。这是一个修改后[配置用例DEMO](https://github.com/lyooyl/AVADatasetMake/blob/main/process_src/slowfast_kinetics400-pretrained-r50_ava22-rgb-sport.py)。
- 训练示例
```shell
python tools/train.py ./my_configs/slowfast_kinetics400-pretrained-r50_ava22-rgb-sport.py
```
- 推理示例
```shell
python demo/demo_spatiotemporal_det.py \
	--config ../work_dirs/slowfast_det_rec_sport-cls4/slowfast_kinetics400-pretrained-r50_8xb6-8x8x1-cosine-10e_ava22-rgb-sport.py \
	--checkpoint ../work_dirs/slowfast_det_rec_sport-cls4/best_mAP_overall_epoch_36.pth \
	--det-config demo/demo_configs/faster-rcnn_r50_fpn_2x_coco_infer.py \
	--det-checkpoint checkpoints/faster_rcnn_r50_fpn_2x_coco_bbox_mAP-0.384_20200504_210434-a5d8aa15.pth  \
	--video ../AVADatasetMake-sport/process_file/videos/bask02.mp4 \
	--out-filename ./demo/testresults/bask02-infer.mp4 \
	--det-score-thr 0.5 \
	--action-score-thr 0.5 \
	--predict-stepsize 4 \
	--output-stepsize 4 \
	--output-fps 6 \
	--label-map ./tools/data/ava/label_map_Custom.txt 
```
- 日志[json分析](https://github.com/lyooyl/AVADatasetMake/blob/main/process_src/my_analyze_logs.py)
```shell
python my_analyze_logs.py \
	--json_log ../work_dirs/slowfast_det_rec_sport-cls4/20230718_111358/vis_data/scalars.json.json
	--keys 'mAP/overall'
```
