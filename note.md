# note

## TODO

* rtm训练道具模型

* 普适标签组合模型
* 3个模型接入labelstadio
* 工程化，补充标注数据，labelstudio一键训练
* 效率优化

## overview

### data

```batch
mklink /D G:\我的云端硬盘\mmdetection\data G:\我的云端硬盘\mmdet_data\
```

### algorithm

* rtmdet - yolov3：
  * 基础的目前是80类（coco）
  * 适合自训练标签，高频、低频

* dino - grounded：
  * 基础识别能力

```bash
python demo/image_demo.py \
  demo/demo.jpg \
  ./configs/grounding_dino/grounding_dino_swin-b_finetune_16xb2_1x_coco.py \
  --weights F:\data\ai\DINO\grounding_dino_swin-b_finetune_16xb2_1x_coco_20230921_153201-f219e0c0.pth \
  --texts 'bench . car .'
```

* blip
  * QVA

* glip
  * comparable to grounded-dino

### dataset

* coco 80
* objects 365
* open images 600
* lvis 1203
* v3det 13029
  * 似乎更适合自然图片，缺少卡通

## training

### 生成数据集

随机背景，3个IP随机出现并随机旋转、随机缩放、随机位置，分为训练集和测试集

### rtmdet tiny

* 针对3个IP生成300train，300val；
* T4训练一个小时
* 效果还可以（coco/bbox_mAP_75: 0.7740，召回率75%的时候准确率0.7740，这里还存在背景里有IP但是没有标注的情况）

```log
10/04 16:54:26 - mmengine - INFO - Epoch(val) [19][60/60] coco/bbox_mAP: 0.6580 coco/bbox_mAP_50: 0.9240 coco/bbox_mAP_75: 0.7740 coco/bbox_mAP_s: -1.0000 coco/bbox_mAP_m: -1.0000 coco/bbox_mAP_l: 0.6580 data_time: 0.2313 time: 1.0160
```

### rtmdet m

* T4: 9.2G RAM, 5.2G GPU
* 300train，300val； 1 hour

```log
10/12 09:08:02 - mmengine - INFO - Epoch(val) [20][60/60]    coco/bbox_mAP: 0.6870  coco/bbox_mAP_50: 0.9240  coco/bbox_mAP_75: 0.8130  coco/bbox_mAP_s: -1.0000  coco/bbox_mAP_m: -1.0000  coco/bbox_mAP_l: 0.6880  data_time: 0.1418  time: 0.9900
```


## reference

https://nbviewer.org/github/chg0901/openmmlab2-hong/blob/main/Assignment3/mmdet_simple_drinks.ipynb