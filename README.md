#【制作AVADataset数据集过程】
```
https://github.com/Whiffe/Custom-ava-dataset_Custom-Spatio-Temporally-Action-Video-Dataset 
（1）代码执行在根目录./AVADatasetMake/下
（2）将输入视频文件放入./process_file/videos/下
```

##【01】、电影剪辑片段
video -- videos_crop
- 修改sh脚本，使输出片段为11s、fps30、n.mp4命名
```shell
./process_src/01_cut_video.sh
```

##02、按片段拆帧					
videos_crop -- frames(全部帧)
```shell
./process_src/02_cut_frames.sh 
```

##【03】、缩减帧
frames -- choose_frames_all & choose_frames -- choose_frames_middle
- 检查sh中的python路径
```shell
./process_src/03_choose_frames.sh	
```

##04、yolo检测
choose_frames_all -- yolov5_det
```shell
./process_src/04_yolo_det.sh
```

##05、pkl生成
yolov5_det/labels -- dense_proposals_train.pkl & dense_proposals_train_deepsort.pkl
```shell
./process_src/05_pkl_gen.sh
```

##【06】、via标注生成
dense_proposals_train.pkl & choose_frames_middle -- _proposal.json
- 修改./process_src/dense_proposals_train_to_via.py的第20行属性字典
```shell
./process_src/06_via_gen.sh	
```
	
##【07】、via软件标注action
_proposal_s.json -- _finish.json
- 下载打开[VIA软件](https://www.robots.ox.ac.uk/~vgg/software/via/downloads/via3/via-3.0.11.zip )，进行行为标注...

##08、via转csv
_finish.json -- train_without_personID.csv
```shell
./process_src/08_via2csv.sh
```

##09、deepsort检测跟踪，生成csv
frames & dense_proposals_train_deepsort.pkl & train_without_personID.csv -- train.csv
```shell
./process_src/09_deepsort_fusion_csv.sh
```

##10、原帧生成
frames -- rawframes
```shell
./process_src/10_rawframes_gen.sh
```

##【11】、其他文件创建

vim action_list.pbtxt # 写入行为列表，例中视频共两种行为，注意有缩进！
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

vim included_timestamps.txt  # 写入时间戳号，视频片段的middle为[02,08]共7帧(没用到)
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
