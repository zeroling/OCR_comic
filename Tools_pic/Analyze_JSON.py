import json

def json_bd(json_data):
    """
    解析 OCR JSON 数据，提取位置信息和文字内容，并返回两个列表：rects 和 texts。
    rects 列表中的每个元素都是一个 xyxy 格式的坐标列表 [x1, y1, x2, y2]，
    texts 列表中的每个元素都是对应的识别出的文字内容。

    :param json_data: OCR JSON 数据字典
    :return: (rects, texts) 元组，其中 rects 是位置坐标列表，texts 是文字内容列表
    """
    # 解析 JSON 数据
    data = json.loads(json_data)
    # 提取位置信息和文字
    rects = []
    texts = []

    for item in data['words_result']:
        location = item['location']
        text = item['words']

        # 计算 xyxy 格式的坐标
        x1, y1 = location['left'], location['top']
        x2, y2 = x1 + location['width'], y1 + location['height']

        rects.append([x1, y1, x2, y2])
        texts.append(text)

    return rects, texts

