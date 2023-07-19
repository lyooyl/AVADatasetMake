default_scope = 'mmaction'
default_hooks = dict(
    runtime_info=dict(type='RuntimeInfoHook'),
    timer=dict(type='IterTimerHook'),
    logger=dict(type='LoggerHook', interval=20, ignore_last=False),
    param_scheduler=dict(type='ParamSchedulerHook'),
    checkpoint=dict(type='CheckpointHook', interval=4, save_best='auto'),
    sampler_seed=dict(type='DistSamplerSeedHook'),
    sync_buffers=dict(type='SyncBuffersHook'))
env_cfg = dict(
    cudnn_benchmark=False,
    mp_cfg=dict(mp_start_method='fork', opencv_num_threads=0),
    dist_cfg=dict(backend='nccl'))
log_processor = dict(type='LogProcessor', window_size=20, by_epoch=True)
vis_backends = [dict(type='LocalVisBackend')]
visualizer = dict(
    type='ActionVisualizer', vis_backends=[dict(type='LocalVisBackend')])
log_level = 'INFO'
load_from = None
resume = False

# url = 'https://download.openmmlab.com/mmaction/recognition/slowfast/slowfast_r50_8x8x1_256e_kinetics400_rgb/slowfast_r50_8x8x1_256e_kinetics400_rgb_20200716-73547d2b.pth'
# num_classes = 8
# custom_classes = [1, 2, 3, 4, 5, 6, 7]
num_classes = 5     # num_class + 1
custom_classes = [1, 2, 3, 4]
model = dict(
    type='FastRCNN',
    _scope_='mmdet',
    # init_cfg=None,
    init_cfg=dict(
        type='Pretrained',
        checkpoint="checkpoints/slowfast_r50_8x8x1_256e_kinetics400_rgb_20200716-73547d2b.pth"
    ),
    backbone=dict(
        type='mmaction.ResNet3dSlowFast',
        resample_rate=4,
        speed_ratio=4,
        channel_ratio=8,
        pretrained=None,
        slow_pathway=dict(
            type='resnet3d',
            depth=50,
            pretrained=None,
            lateral=True,
            conv1_kernel=(1, 7, 7),
            dilations=(1, 1, 1, 1),
            conv1_stride_t=1,
            pool1_stride_t=1,
            inflate=(0, 0, 1, 1),
            spatial_strides=(1, 2, 2, 1),
            fusion_kernel=7),
        fast_pathway=dict(
            type='resnet3d',
            depth=50,
            pretrained=None,
            lateral=False,
            base_channels=8,
            conv1_kernel=(5, 7, 7),
            conv1_stride_t=1,
            pool1_stride_t=1,
            spatial_strides=(1, 2, 2, 1))),
    roi_head=dict(
        type='AVARoIHead',
        bbox_roi_extractor=dict(
            type='SingleRoIExtractor3D',
            roi_layer_type='RoIAlign',
            output_size=8,
            with_temporal_pool=True),
        bbox_head=dict(
            type='BBoxHeadAVA',
            in_channels=2304,
            # num_classes=81,
            num_classes=num_classes,
            topk=(1, 3),        # 两类topk=1即可，大于5类按默认topk=(3, 5)

            multilabel=True,
            dropout_ratio=0.5)),
    data_preprocessor=dict(
        type='mmaction.ActionDataPreprocessor',
        mean=[123.675, 116.28, 103.53],
        std=[58.395, 57.12, 57.375],
        format_shape='NCTHW'),
    train_cfg=dict(
        rcnn=dict(
            assigner=dict(
                type='MaxIoUAssignerAVA',
                pos_iou_thr=0.9,
                neg_iou_thr=0.9,
                min_pos_iou=0.9),
            sampler=dict(
                type='RandomSampler',
                num=32,
                pos_fraction=1,
                neg_pos_ub=-1,
                add_gt_as_proposals=True),
            pos_weight=1.0)),
    test_cfg=dict(rcnn=None))

dataset_type = 'AVADataset'
data_root = '../AVADatasetMake-sport/ava_finally/rawframes'         # 生成的视频帧图
anno_root = '../AVADatasetMake-sport/ava_finally/annotations'

ann_file_train = f'{anno_root}/train.csv'
ann_file_val = f'{anno_root}/train.csv'

exclude_file_train = f'{anno_root}/train_excluded_timestamps.csv'
exclude_file_val = f'{anno_root}/train_excluded_timestamps.csv'

label_file = f'{anno_root}/action_list.pbtxt'

proposal_file_train = f'{anno_root}/dense_proposals_train.pkl'
proposal_file_val = f'{anno_root}/dense_proposals_train.pkl'

file_client_args = dict(io_backend='disk')

train_pipeline = [
    dict(type='SampleAVAFrames', clip_len=32, frame_interval=2),
    dict(type='RawFrameDecode', io_backend='disk'),
    dict(type='RandomRescale', scale_range=(256, 320)),
    dict(type='RandomCrop', size=256),
    dict(type='Flip', flip_ratio=0.5),
    dict(type='FormatShape', input_format='NCTHW', collapse=True),
    dict(type='PackActionInputs')
]
val_pipeline = [
    dict(
        type='SampleAVAFrames', clip_len=32, frame_interval=2, test_mode=True),
    dict(type='RawFrameDecode', io_backend='disk'),
    dict(type='Resize', scale=(-1, 256)),
    dict(type='FormatShape', input_format='NCTHW', collapse=True),
    dict(type='PackActionInputs')
]
train_dataloader = dict(
    batch_size=2,
    num_workers=8,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    dataset=dict(
        type=dataset_type,
        ann_file=ann_file_train,
        exclude_file=exclude_file_train,
        pipeline=train_pipeline,
        label_file=label_file,
        proposal_file=proposal_file_train,
        data_prefix=dict(img=data_root),
        # 自定义类别（标签、数目）
        custom_classes=custom_classes,
        num_classes=num_classes
        )
    )
val_dataloader = dict(
    batch_size=1,
    num_workers=8,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type=dataset_type,
        ann_file=ann_file_val,
        exclude_file=exclude_file_val,
        pipeline=val_pipeline,
        label_file=label_file,
        proposal_file=proposal_file_val,
        data_prefix=dict(img=data_root),
        # 自定义类别（标签、数目）
        custom_classes=custom_classes,
        num_classes=num_classes,
        test_mode=True))
test_dataloader = val_dataloader

val_evaluator = dict(
    type='AVAMetric',
    ann_file=ann_file_val,
    label_file=label_file,
    exclude_file=exclude_file_val,
     # 自定义类别（标签、数目）
    custom_classes=custom_classes,
    num_classes=num_classes
    )
test_evaluator = val_evaluator

train_cfg = dict(
    type='EpochBasedTrainLoop', max_epochs=60, val_begin=1, val_interval=4)
val_cfg = dict(type='ValLoop')
test_cfg = dict(type='TestLoop')
param_scheduler = [
    dict(
        type='LinearLR',
        start_factor=0.1,
        by_epoch=True,
        begin=0,
        end=2,
        convert_to_iter_based=True),
    dict(
        type='CosineAnnealingLR',
        T_max=8,
        eta_min=0,
        by_epoch=True,
        begin=2,
        end=10,
        convert_to_iter_based=True)
]
optim_wrapper = dict(
    optimizer=dict(type='SGD', lr=0.075, momentum=0.9, weight_decay=1e-05),
    clip_grad=dict(max_norm=40, norm_type=2))
auto_scale_lr = dict(enable=False, base_batch_size=48)
launcher = 'none'
work_dir = '../work_dirs/slowfast_det_rec_sport-cls4'
randomness = dict(seed=None, diff_rank_seed=False, deterministic=False)
