import time
import os
import cv2

from Tools_pic.Draw_rect import draw_rectangles_and_text
from Tools_pic.ocr_bd_v1 import ocr_bd_v1
from Tools_pic.ocr_bd_v2 import ocr_bd_v2
from Tools_pic.ocr_dy_v1 import ocr_dy_v1
from Tools_pic.Translate_pic import translate


ID_dy = ''
KeyID_dy = ''

ID_bd = ""
KeyID_bd = ""

image_path = "3f3f726729cc298bfe5fc238af6ea02.png"  # 图像文件路径
output_path = "output_with_boxes.png"  # 输出文件路径




def ocr(input_folder, output_folder, Flag):
    def run_ocr(flag, ID_dy, KeyID_dy, ID_bd, KeyID_bd, image_path):
        if flag == 'dy':
            return ocr_dy_v1(ID_dy, KeyID_dy, image_path)
        elif flag == 'bd_v1':
            return ocr_bd_v1(ID_bd, KeyID_bd, image_path)
        elif flag == 'bd_v2':
            return ocr_bd_v2(ID_bd, KeyID_bd, image_path)
        else:
            raise ValueError("Invalid flag value. Expected 'dy', 'bd_v1', or 'bd_v2'.")
    """
    从 input_folder 中读取所有图片，进行 OCR 识别、翻译，并将结果保存到 output_folder。
    :param input_folder: 输入图片所在的文件夹路径
    :param output_folder: 处理后的图片保存的文件夹路径
    """
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            # 进行 OCR 识别
            merged_rects, merged_texts = run_ocr(Flag, ID_dy, KeyID_dy, ID_bd, KeyID_bd, image_path)
            time.sleep(2)
            # 翻译文字
            zh_text = translate(merged_texts, 'zh', ID_dy, KeyID_dy)
            # 绘制矩形框和中文文本
            image = draw_rectangles_and_text(image_path, merged_rects, zh_text, "SimHei.ttf", 30)
            # 保存带有标注的新图像
            cv2.imwrite(output_path, image)


if __name__ == '__main__':
    '''推荐字节API或者百度的V2版本,即OCR高精度带坐标版,三个版本,dy,bd_v1,bd_v2,这里推荐bd_v1,翻译使用的是字节的api,每月200w字免费额度'''
    ocr(r"C:\Users\16406\Desktop\new", "Test_dy_v1", "dy")
