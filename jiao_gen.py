## 随机ip，随机背景，随机位置
import json
import os
import random

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter


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
        # 获取背景图片的宽度和高度
        bg_width, bg_height = img_bg.size
        # 获取要添加的图片的宽度和高度

        # 1、随机旋转
        img_ip_processed = rotate_img(img_ip)

        # 2. 缩放
        img_ip_processed = resize_img(img_ip_processed)

        # 3. 模糊、遮挡、变色
        img_ip_processed = effect_img(img_ip_processed)

        # 4、将要添加的图片粘贴到背景图片的随机位置
        ip_width, ip_height = img_ip_processed.size
        x = random.randint(0, bg_width - ip_width)
        y = random.randint(0, bg_height - ip_height)
        #
        img_bg.paste(img_ip_processed, (x, y), img_ip_processed)

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
        categories=[{"id": 0, "name": "jiaojiao"}],
    )
    with open(f"{dir_dist}/{gen_type}.json", "w", encoding="utf8") as json_file:
        json.dump(coco_format_json, json_file)

    return i_anno


def resize_img(img_in):
    scale_factor = random.uniform(0.7, 1.3)
    new_width = int(img_in.width * scale_factor)
    new_height = int(img_in.height * scale_factor)
    return img_in.resize((new_width, new_height))


def rotate_img(img_in):
    rotation_angle = random.randint(-30, 30)
    return img_in.rotate(rotation_angle, expand=True)


# 一定程度模糊、遮挡、变色
def effect_img(img_in):
    img_processed = img_in
    if random.randint(0, 100) > 80:
        img_processed = img_processed.filter(ImageFilter.BLUR)

    if random.randint(0, 100) > 90:
        width, height = img_processed.size

        draw = ImageDraw.Draw(img_processed)
        scale_factor = random.uniform(2, 5)
        wDraw = int(width / scale_factor)
        hDraw = int(height / scale_factor)

        x1 = random.randint(0, width - wDraw)  # 遮挡矩形左上角 x 坐标
        y1 = random.randint(0, height - hDraw)  # 遮挡矩形左上角 y 坐标
        x2 = x1 + wDraw  # 遮挡矩形右下角 x 坐标
        y2 = y1 + hDraw  # 遮挡矩形右下角 y 坐标
        draw.rectangle((x1, y1, x2, y2), fill="black")

    if random.randint(0, 100) > 80:
        enhancer = ImageEnhance.Color(img_processed)
        img_processed = enhancer.enhance(2.0)

    return img_processed


if __name__ == "__main__":
    dir_dist = r"./data/jiao2"
    do_gen(
        dir_ip=r"D:\data\ai\jiao\V1\IP\叫叫",
        dir_scene=r"D:\data\ai\jiao\V1\scene\场景",
        dir_dist=dir_dist,
        gen_type="train",
        i_img=1,
        i_anno=1,
        n=300,
    )
    do_gen(
        dir_ip=r"D:\data\ai\jiao\V1\IP\叫叫",
        dir_scene=r"D:\data\ai\jiao\V1\scene\场景",
        dir_dist=dir_dist,
        gen_type="val",
        i_img=1,
        i_anno=1,
        n=300,
    )
