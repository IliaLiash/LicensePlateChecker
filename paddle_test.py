from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import cv2
import numpy as np
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# to switch the language model in order.


def paddle_ocr_recognition_img(img_path='./plates/volvo.jpg'):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')  # need to run only once to download and load model into memory
    result = ocr.ocr(img_path, cls=True)
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            print(line)

    result = result[0]
    image = Image.open(img_path).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, txts, scores, font_path='simfang.ttf')
    # print(scores)
    im_show = Image.fromarray(im_show)
    im_show.save('result.jpg')
    return txts


def paddle_ocr_recognition_video(video_source='./plates/vid.mp4'):
    capture = cv2.VideoCapture(video_source)
    ocr = PaddleOCR(use_angle_cls=True, lang='en')

    while True:
        _, image = capture.read()
        # image = cv2.resize(image, (600, 400))

        result = ocr.ocr(image, cls=True)
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                print(line)

        result = result[0]
        # img = Image.open(image).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        im_show = draw_ocr(image, boxes, txts, scores, font_path='simfang.ttf')
        # im_show = Image.fromarray(im_show)
        # im_show.save('result.jpg')
        open_cv_image = np.array(im_show)

        cv2.imshow("Image", open_cv_image)
        cv2.waitKey(10)


if __name__ == "__main__":
    paddle_ocr_recognition_img()
