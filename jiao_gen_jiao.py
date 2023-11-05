## 随机ip，随机背景，随机位置
import json
import os
import random

from PIL import Image

from toolkit import *


def do_gen(
    dir_ip=r"D:\data\ai\jiao\V1\IP\叫叫",
    dir_scene=r"D:\data\ai\jiao\V1\scene\场景",
    dir_dist=r"./data/jiao",
    gen_type="train",
    i_img=1,
    i_anno=1,
    n=100,
):
    list_ip_fn = os.listdir(dir_ip)
    list_scene_fn = os.listdir(dir_scene)
    os.makedirs(dir_dist, exist_ok=True)
    os.makedirs(f"{dir_dist}/{gen_type}", exist_ok=True)

    images = []
    annotations = []
    for i in range(n):
        fn_ip = list_ip_fn[random.randint(1, len(list_ip_fn)) - 1]
        fullpath_ip = f"{dir_ip}/{fn_ip}"
        fullpath_scene = (
            f"{dir_scene}/{list_scene_fn[random.randint(1, len(list_scene_fn))-1]}"
        )
        print(f"try to place {fullpath_ip} in {fullpath_scene}")

        img_bg = Image.open(fullpath_scene)
        img_ip = Image.open(fullpath_ip)

        # 1、随机旋转
        img_ip_processed = rotate_img(img_ip)

        # 2. 缩放
        img_ip_processed = resize_img(img_ip_processed)

        # 3. 模糊、遮挡、变色
        img_ip_processed = effect_img(img_ip_processed)

        # 4、将要添加的图片粘贴到背景图片的随机位置
        img_bg = paste_img(img_bg, img_ip_processed)

        # 获取背景图片的宽度和高度
        bg_width, bg_height = img_bg.size
        # 获取要添加的图片的宽度和高度
        ip_width, ip_height = img_ip_processed.size

        # 保存合成后的图片
        img_bg = img_bg.convert("RGB")
        img_bg.save(f"{dir_dist}/{gen_type}/{i}.jpg")

        # 图像信息
        image_info = dict(
            id=i,
            file_name=f"{i}.jpg",
            height=bg_height,
            width=bg_width,
        )
        images.append(image_info)
        # 矩形框信息
        annotation_info = dict(
            image_id=i,
            id=i_anno,
            category_id=0,
            bbox=[x, y, ip_width, ip_height],
            area=ip_width * ip_height,
            # segmentation=[],
            iscrowd=0,
        )
        annotations.append(annotation_info)

        i_anno += 1
        # break

    coco_format_json = dict(
        images=images,
        annotations=annotations,
        categories=[
            {"id": 0, "name": "叫叫"},
            {"id": 1, "name": "猪小弟"},
            {"id": 2, "name": "铃铛"},
        ],
    )
    with open(f"{dir_dist}/{gen_type}.json", "w", encoding="utf8") as json_file:
        json.dump(coco_format_json, json_file)

    return i_anno


if __name__ == "__main__":
    dir_dist = r"./data/jiao"
    do_gen(
        dir_ip=r"D:\data\ai\jiao\V1\IP\叫叫",
        dir_scene=r"D:\data\ai\jiao\V1\scene\场景",
        dir_dist=dir_dist,
        gen_type="train",
        i_img=1,
        i_anno=1,
        n=1,
    )
    do_gen(
        dir_ip=r"D:\data\ai\jiao\V1\IP\叫叫",
        dir_scene=r"D:\data\ai\jiao\V1\scene\场景",
        dir_dist=dir_dist,
        gen_type="val",
        i_img=1,
        i_anno=1,
        n=1,
    )
