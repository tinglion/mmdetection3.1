import json
import os
import random

from PIL import Image

from conf import *
from toolkit import *


# TODO 每个道具，n个随机背景，随机特效
def do_gen_prop(
    dir_prop=default_dir_prop,
    dir_scene=default_dir_scene,
    dir_dist=r"./data/jiao",
    gen_type="train",
    n=1,
):
    list_prop = os.listdir(dir_prop)
    list_scene = os.listdir(dir_scene)
    os.makedirs(dir_dist, exist_ok=True)
    os.makedirs(f"{dir_dist}/{gen_type}", exist_ok=True)

    categories = []
    for prop in list_prop:
        categories.append(
            {"id": len(categories), "name": prop, "path": f"{dir_prop}/{prop}"}
        )

    images = []
    annotations = []
    for cat in categories:
        print(f"try prop {cat}")

        for i in range(0, n):
            img_id = len(images) + 1

            i_scene = random.randint(0, len(list_scene) - 1)
            fullpath_scene = f"{dir_scene}/{list_scene[i_scene]}"
            print(f"    {img_id} {i} {fullpath_scene} ({i_scene})")

            img_bg = Image.open(fullpath_scene)
            img_bg = img_bg.convert("RGB")

            img_processed = Image.open(cat["path"])

            img_bg, img_processed, (x, y) = process_img(img_bg, img_processed)
            ip_width, ip_height = img_processed.size

            # 保存合成后的图片
            img_bg.save(f"{dir_dist}/{gen_type}/{img_id}.jpg")

            # 图像信息
            image_info = dict(
                id=img_id,
                file_name=f"{img_id}.jpg",
                height=img_bg.height,
                width=img_bg.width,
            )
            images.append(image_info)

            # 矩形框信息
            annotation_info = dict(
                image_id=img_id,
                id=len(annotations) + 1,
                category_id=cat["id"],
                bbox=[x, y, ip_width, ip_height],
                area=ip_width * ip_height,
                # segmentation=[],
                iscrowd=0,
            )
            annotations.append(annotation_info)
        # break

    coco_format_json = dict(
        images=images,
        annotations=annotations,
        categories=categories,
    )
    with open(f"{dir_dist}/{gen_type}.json", "w", encoding="utf8") as json_file:
        json.dump(coco_format_json, json_file, ensure_ascii=False)

    return len(annotations)


if __name__ == "__main__":
    dir_dist = r"./data/prop"

    do_gen_prop(
        dir_prop=default_dir_prop,
        dir_scene=default_dir_scene,
        dir_dist=dir_dist,
        gen_type="train",
        n=5,
    )
    do_gen_prop(
        dir_prop=default_dir_prop,
        dir_scene=default_dir_scene,
        dir_dist=dir_dist,
        gen_type="val",
        n=5,
    )
