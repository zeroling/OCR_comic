import base64
from io import BytesIO
from PIL import Image

def image_rgb(image):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image_resize = resize(image, max_size=2048)
    return image_resize

def resize(image, max_size=2048):
    # 原图的宽、高
    w, h = image.width, image.height
    max_wh = max(w, h)
    if max_wh < max_size:
        return image

    ratio = float(max_size) / (max(float(w), float(h)))
    width = int(w * ratio)
    height = int(h * ratio)

    # resample: 图像插值算法
    # Image.Resampling.NEAREST: 最近邻插值
    # Image.Resampling.BILINEAR: 双线性插值
    # Image.Resampling.BICUBIC: 双三次插值
    return image.resize(size=(width, height), resample=Image.Resampling.NEAREST)


def base64_to_image(image):
    # 1、根据Exif中的方向信息把图片转成正向
    # 2、图片缩放，长边最大到2048
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    encoded_string = base64.b64encode(buffered.getvalue()).decode()
    return encoded_string