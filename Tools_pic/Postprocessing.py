def process_inf(ocr_infos):
    def convert_to_xyxy(rects):
        """将矩形列表转换为 xyxy 格式"""
        x1, y1 = rects[0]  # 左上角坐标
        x2, y2 = rects[2]  # 右下角坐标
        return [x1, y1, x2, y2]

    def sort_rect_coordinates(rect):
        """对矩形框的坐标进行排序，确保左上角坐标在前"""
        # 按照y坐标升序排列，如果y坐标相同，则按x坐标升序排列
        sorted_coords = sorted(rect, key=lambda coord: (coord[1], coord[0]))
        # 确保左上角坐标在第一个位置
        top_left = sorted_coords[0]
        bottom_right = max(sorted_coords[1:], key=lambda coord: (coord[0], coord[1]))
        return [top_left, [top_left[0], bottom_right[1]], bottom_right, [bottom_right[0], top_left[1]]]

    rects = []
    texts = []
    for item in ocr_infos:
        texts.append(item['text'])
        rects.append(convert_to_xyxy(sort_rect_coordinates(item['rect'])))
    return rects, texts


def are_centers_close(rect1, rect2):
    """判断两个矩形框中心点是否接近"""
    def center_distance(rect1, rect2):
        """计算两个矩形框中心点之间的距离"""
        x1, y1 = (rect1[0] + rect1[2]) / 2, rect1[1]
        x2, y2 = (rect2[0] + rect2[2]) / 2, rect2[1]
        return abs(x1 - x2), abs(y1 - y2)

    dx, dy = center_distance(rect1, rect2)
    w1, h1 = rect1[2] - rect1[0], rect1[3] - rect1[1]
    w2, h2 = rect2[2] - rect2[0], rect2[3] - rect2[1]

    max_dx = (w1 + w2) * 1.5 / 2
    max_dy = (h1 + h2) / 4

    return dx <= max_dx and dy <= max_dy

def merge_rects_and_texts(rects, texts):
    """递归合并接近的矩形框及其对应的文本"""
    def merge_helper(rects, texts):
        if len(rects) <= 1:
            return rects, texts

        def merge_rectangles(rect1, rect2):
            """合并两个矩形框"""
            x1 = min(rect1[0], rect2[0])
            y1 = min(rect1[1], rect2[1])
            x2 = max(rect1[2], rect2[2])
            y2 = max(rect1[3], rect2[3])
            return [x1, y1, x2, y2]

        def merge_texts(text_pairs):
            """合并两个文本，右边的文本在前"""
            (rect1, text1), (rect2, text2) = text_pairs
            if (rect1[2] + rect1[0]) / 2 > (rect2[2] + rect2[0]) / 2:
                return text1 + text2
            else:
                return text2 + text1

        for i in range(len(rects)):
            for j in range(i + 1, len(rects)):
                if are_centers_close(rects[i], rects[j]):
                    merged_rect = merge_rectangles(rects[i], rects[j])
                    merged_text = merge_texts([(rects[i], texts[i]), (rects[j], texts[j])])
                    new_rects = rects[:i] + rects[i + 1:j] + rects[j + 1:]
                    new_texts = texts[:i] + texts[i + 1:j] + texts[j + 1:]
                    new_rects.insert(i, merged_rect)
                    new_texts.insert(i, merged_text)
                    return merge_helper(new_rects, new_texts)

        return rects, texts
    return merge_helper(rects, texts)



def adjust_boxes_from_images(boxes, resized_image, original_image):
    """
    根据两个 Image 对象调整矩形框坐标以适应原始图像尺寸。

    参数:
    - boxes: 列表，包含矩形框的坐标，每个矩形框由四个整数表示 (x1, y1, x2, y2)。
    - resized_image: Image 对象，resize后的图像。
    - original_image: Image 对象，原始图像。

    返回:
    - 调整后的矩形框坐标列表。
    """

    # 获取尺寸
    resized_width, resized_height = resized_image.size
    original_width, original_height = original_image.size

    # 计算比例
    width_ratio = original_width / resized_width
    height_ratio = original_height / resized_height

    # 调整坐标
    def adjust_coordinates(box):
        return [
            int(box[0] * width_ratio),
            int(box[1] * height_ratio),
            int(box[2] * width_ratio),
            int(box[3] * height_ratio)
        ]

    # 应用调整
    adjusted_boxes = [adjust_coordinates(box) for box in boxes]

    return adjusted_boxes

