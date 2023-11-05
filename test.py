import glob

from mmdet.apis import DetInferencer

# # Choose to use a config
# config = 'dino-5scale_swin-l_8xb2-12e_coco.py.py'
# # Setup a checkpoint file to load
# checkpoint = glob.glob('dino-5scale_swin-l_8xb2-12e_coco_20230228_072924-a654145f.pth')[0]


# config = r".\configs\v3det\dino-4scale_swin_16xb1_sample1e-3_v3det_36e.py"
# model_file = r"F:\data\ai\DINO\dino_swin_420.pth"

# config = r".\configs\grounding_dino\grounding_dino_swin-b_finetune_16xb2_1x_coco.py"
# model_file = r"F:\data\ai\DINO\grounding_dino_swin-b_finetune_16xb2_1x_coco_20230921_153201-f219e0c0.pth"

# config = r"configs/rtmdet/rtmdet_m_8xb32-300e_coco.py"
# model_file = r"..\mmdet_checkpoints\rtmdet_m_8xb32-300e_coco_20220719_112220-229f527c.pth"

# config = r"configs/rtmdet/rtmdet_x_8xb32-300e_coco.py"
# model_file = r"..\mmdet_checkpoints\rtmdet_x_8xb32-300e_coco_20220715_230555-cc79b9ae.pth"

# config = 'configs/rtmdet/jiao_conf.py'
# checkpoint = glob.glob('work_dirs/jiao_conf/best_coco_bbox_mAP_epoch_11.pth')[0]

# config = 'configs/rtmdet/jiao_ip3_conf.py'
# checkpoint = glob.glob('work_dirs/jiao_ip3_conf/best_coco_bbox_mAP_epoch_19.pth')[0]

# config = r"configs/rtmdet/jiao_m_ip3_300_conf.py"
# model_file = r"work_dirs/jiao_m_ip3_300_conf/best_coco_bbox_mAP_epoch_20.pth"

config = r"configs/rtmdet/jiao_l_ip3_300_conf.py"
model_file = r"work_dirs/jiao_l_ip3_300_conf/best_coco_bbox_mAP_epoch_20.pth"

# Set the device to be used for evaluation
device = "cpu"  # 'cuda:0'

# Initialize the DetInferencer
checkpoint = glob.glob(model_file)[0]
inferencer = DetInferencer(config, checkpoint, device)

# Use the detector to do inference
img = "./data/ip3/val/1.jpg"
# img = r"F:\data\ai\v3det\images\Q98669453\24_319_5490564790_b6ba59a5ef_c.jpg"
result = inferencer(img, out_dir="./outputs")
