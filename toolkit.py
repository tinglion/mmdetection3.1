import json
import os
import random

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter


def process_img(img_bg, img_ip_processed):
    bg_width, bg_height = img_bg.size

    # 1. 缩放
    img_ip_processed = resize_img(
        img_ip_processed, max_size=[int(bg_width / 2), int(bg_height / 2)]
    )

    # 2、旋转
    img_ip_processed = rotate_img(img_ip_processed)

    # 3. 模糊、遮挡、变色
    img_ip_processed = effect_img(img_ip_processed)

    # 4、将要添加的图片粘贴到背景图片的随机位置
    ip_width, ip_height = img_ip_processed.size
    x = random.randint(0, bg_width - ip_width)
    y = random.randint(0, bg_height - ip_height)
    #
    img_bg.paste(img_ip_processed, (x, y), img_ip_processed)
    return img_bg, img_ip_processed, (x, y)


def resize_img(img_in, max_size=[2000, 2000]):
    scale_factor = random.uniform(0.7, 1.3)

    scale_factor = min(scale_factor, max_size[0] / img_in.width)
    scale_factor = min(scale_factor, max_size[1] / img_in.height)

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
