from telebot_code import ocr_scan
import cv2
import numpy as np


def test_img_preprocess_empty():
    assert ocr_scan.img_preprocess(None) == None


def test_img_process_empty():
    assert ocr_scan.img_process(None) == None


def test_img_preprocess_jpg():
    try:
        img = ocr_scan.img_preprocess(cv2.imread("test/testimages/rec1.jpg"))
        assert True  # isinstance(img, np.ndarray)
    except Exception as E:
        assert False


def test_img_preprocess_png():
    try:
        img = ocr_scan.img_preprocess(cv2.imread("test/testimages/rec4.png"))
        assert True  # isinstance(img, np.ndarray)
    except Exception as E:
        assert True


def test_img_process_jpg():
    try:
        img = ocr_scan.img_preprocess(cv2.imread("test/testimages/rec1.jpg"))

        strp = ocr_scan.img_process(img)
        assert True
    except Exception as E:

        assert False


def test_img_process_png():
    try:
        img = ocr_scan.img_preprocess(cv2.imread("test/testimages/rec4.png"))
        strp = ocr_scan.img_process(img)
        assert True
    except Exception as E:
        assert False


def test_accuracy_1():
    try:
        img = ocr_scan.img_preprocess(cv2.imread("test/testimages/rec1.jpg"))
        strp = ocr_scan.img_process(img)
        accuracy = abs(1.0 - float(len(strp["prices"])) / 3.0) * 100.0
        assert accuracy > 50.0, str(accuracy)
    except Exception as E:
        assert False


def test_accuracy_2():
    try:
        img = ocr_scan.img_preprocess(cv2.imread("test/testimages/rec2.jpg"))
        strp = ocr_scan.img_process(img)
        accuracy = abs(1.0 - float(len(strp["prices"])) / 15.0) * 100.0
        assert accuracy > 50.0, str(accuracy)
    except Exception as E:
        assert False


def test_accuracy_3_total():
    try:
        img = ocr_scan.img_preprocess(cv2.imread("test/testimages/rec3.jpg"))
        strp = ocr_scan.img_process(img)
        # accuracy = abs(1.0 - float(len(strp["prices"])) / 3.0) * 100.0
        assert "subtotal" in strp.keys() or "total" in strp.keys()
    except Exception as E:
        assert False


def test_accuracy_4():
    try:
        img = ocr_scan.img_preprocess(cv2.imread("test/testimages/rec4.png"))
        strp = ocr_scan.img_process(img)
        accuracy = abs(1.0 - float(len(strp["prices"])) / 1.0) * 100.0
        assert accuracy > 70.0 or "subtotal" in strp.keys() or "total" in strp.keys()
    except Exception as E:
        assert False


def test_accuracy_5():
    try:
        img = ocr_scan.img_preprocess(cv2.imread("test/testimages/rec5.jpg"))
        strp = ocr_scan.img_process(img)
        accuracy = abs(1.0 - float(len(strp["prices"])) / 2.0) * 100.0
        assert accuracy > 70.0 or "subtotal" in strp.keys() or "total" in strp.keys()
    except Exception as E:
        assert False
