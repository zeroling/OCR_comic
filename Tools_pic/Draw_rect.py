from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np

def draw_rectangles_and_text(image_path, rectangles, texts, font_path, font_size):
    """
    在给定的图像上绘制矩形并添加竖向排列的中文文本。

    :param image: 输入的背景图像 (OpenCV格式)
    :param rectangles: 包含矩形坐标的列表，每个元素是一个[x1, y1, x2, y2]的列表
    :param texts: 包含对应文本的列表
    :param font_path: 中文字体文件路径
    """
    # 加载中文字体
    font = ImageFont.truetype(font_path, size=font_size)  # 字体大小可以根据需要调整
    # 将图像转换为PIL格式
    pil_image = Image.fromarray(cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB))
    # 创建绘图对象
    draw = ImageDraw.Draw(pil_image)
    # 遍历每个矩形
    for i, (x1, y1, x2, y2) in enumerate(rectangles):
        # 绘制矩形
        draw.rectangle([(x1, y1), (x2, y2)], fill=(255, 255, 255))  # 黑色填充矩形
        # 计算文本位置
        text_x = x2 - font_size
        text_y = y1  # 文本起始位置，这里假设字体大小为20
        # 分割文本，逐字符绘制
        for char in texts[i]:
            if text_y + font_size > y2:  # 如果超出矩形高度
                text_x -= font_size  # 横向回退
                text_y = y1  # 重置到起始y位置
            draw.text((text_x, text_y), char, font=font, fill=(0, 0, 0))  # 黑色文本
            text_y += font_size  # 下移文本位置
    # 将PIL图像转换回OpenCV格式
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    return image

