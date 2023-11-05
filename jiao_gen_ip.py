import json
import os
import random

from PIL import Image

from conf import *
from toolkit import *


## n个图片，随机背景，随机ip，随机位置，随机特效
def do_gen(
    ips,
    dir_ip=r"D:\data\ai\jiao\V1\IP",
    dir_scene=r"D:\data\ai\jiao\V1\scene\场景",
    dir_dist=r"./data/jiao",
    gen_type="train",
    i_img=1,
    i_anno=1,
    n=100,
):
    list_ip_fn = []
    for cat in ips:
        path = f"{dir_ip}/{cat['name']}"
        list_ip_fn.append(
            {
                "id": cat["id"],
                "name": cat["name"],
                "path": path,
                "filelist": os.listdir(path),
            }
        )
    # print(f"{list_ip_fn}")
    list_scene_fn = os.listdir(dir_scene)
    os.makedirs(dir_dist, exist_ok=True)
    os.makedirs(f"{dir_dist}/{gen_type}", exist_ok=True)

    images = []
    annotations = []
    for i in range(i_img, i_img + n):
        scene_i = random.randint(0, len(list_scene_fn) - 1)
        fullpath_scene = f"{dir_scene}/{list_scene_fn[scene_i]}"
        print(f"{i} {fullpath_scene} ({scene_i})")
        img_bg = Image.open(fullpath_scene)
        img_bg = img_bg.convert("RGB")
        bg_width, bg_height = img_bg.size

        for ip_fns in list_ip_fn:
            if random.randint(1, 100) > 60:
                continue
            pic_i = random.randint(0, len(ip_fns["filelist"]) - 1)
            fullpath_ip = f"{ip_fns['path']}/{ip_fns['filelist'][pic_i]}"
            print(f"    place {i_anno} {fullpath_ip}")
            img_ip_processed = Image.open(fullpath_ip)

            img_bg, img_ip_processed, (x, y) = process_img(img_bg, img_ip_processed)
            ip_width, ip_height = img_ip_processed.size

            # 矩形框信息
            annotation_info = dict(
                image_id=i,
                id=i_anno,
                category_id=ip_fns["id"],
                bbox=[x, y, ip_width, ip_height],
                area=ip_width * ip_height,
                # segmentation=[],
                iscrowd=0,
            )
            annotations.append(annotation_info)
            i_anno += 1

        # 保存合成后的图片
        img_bg.save(f"{dir_dist}/{gen_type}/{i}.jpg")

        # 图像信息
        image_info = dict(
            id=i,
            file_name=f"{i}.jpg",
            height=bg_height,
            width=bg_width,
        )
        images.append(image_info)
        # break

    coco_format_json = dict(
        images=images,
        annotations=annotations,
        categories=ips,
    )
    with open(f"{dir_dist}/{gen_type}.json", "w", encoding="utf8") as json_file:
        json.dump(coco_format_json, json_file, ensure_ascii=False)

    return i_anno


if __name__ == "__main__":
    dir_dist = r"./data/ip3"

    do_gen(
        ips=default_ips,
        dir_ip=default_dir_ip,
        dir_scene=default_dir_scene,
        dir_dist=dir_dist,
        gen_type="train",
        i_img=1,
        i_anno=1,
        n=300,
    )
    do_gen(
        ips=default_ips,
        dir_ip=default_dir_ip,
        dir_scene=default_dir_scene,
        dir_dist=dir_dist,
        gen_type="val",
        i_img=1,
        i_anno=1,
        n=300,
    )
