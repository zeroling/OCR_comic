import os

from PIL import Image
from volcengine.visual.VisualService import VisualService

from Tools_pic.Postprocessing import process_inf, merge_rects_and_texts, adjust_boxes_from_images
from Tools_pic.Preprocessing import resize, base64_to_image, image_rgb


def ocr_dy_v1(ID, Key, filename):
    visual_service = VisualService()
    visual_service.set_ak(ID)
    visual_service.set_sk(Key)  # 密钥省略部分
    action = "MultiLanguageOCR"
    version = "2022-08-31"
    visual_service.set_api_info(action, version)
    # 获取图片完整路径
    image_path = os.path.join(os.getcwd(), filename)
    image_original = image_rgb(Image.open(image_path))
    image_resize = resize(image_original, max_size=2048)
    form = {"image_base64": base64_to_image(image_resize)}
    resp = visual_service.ocr_api(action, form)
    return process_and_merge_ocr_info(resp, image_resize, image_original)

def process_and_merge_ocr_info(resp, image1, image2):
    # 从响应数据中提取矩形区域和文本
    rects, texts = process_inf(resp['data']['ocr_infos'])
    # 合并矩形区域和对应的文本
    merged_rects, merged_texts = merge_rects_and_texts(rects, texts)
    # 因为图片被压缩,返回的坐标是压缩后的坐标,需要调整
    true_rect = adjust_boxes_from_images(merged_rects, image1, image2)
    return true_rect, merged_texts