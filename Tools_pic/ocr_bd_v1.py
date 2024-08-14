import base64
import urllib

import requests

from Tools_pic.Analyze_JSON import json_bd
from Tools_pic.Postprocessing import merge_rects_and_texts


def ocr_bd_v1(API_kEY, SECRET_KEY,image_path):
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=" + get_access_token(API_kEY, SECRET_KEY)
    image_base64 = get_file_content_as_base64(image_path, True)
    payload = f'image={image_base64}&language_type=JAP&detect_direction=false&detect_language=false&vertexes_location=false&paragraph=false&probability=false'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    rects, texts = json_bd(response.text)
    return merge_rects_and_texts(rects, texts)


def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


def get_access_token(API_KEY, SECRET_KEY):
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

