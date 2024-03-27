import pcat_config
import cv2 as cv
import base64
from pathlib import Path
from datetime import datetime
import os

CAP_IMG_PATH = os.path.join(Path(__file__).resolve().parent, '../captures')


def __frame_to_base64__(frame):
    """Convert a opencv captured frame(numpy array) to base64 string"""
    return str(base64.b64encode(frame))


def capture_camera(camera_src):
    """Capture a frame from a specific camera"""
    if camera_src < 0 or camera_src == '':
        return ""

    captured_frame_base64 = ""
    try:
        cap = cv.VideoCapture(camera_src)
        if cap.isOpened():
            print('Begin capturing...')
            ret, frame = cap.read()

            if ret:
                print('Capture succeed')
                # For debug only
                dt_now = datetime.now()
                str_file_name = '{0}.jpg'.format(dt_now.strftime('%Y%m%d%H%M%S'))
                str_image_save_path = os.path.join(CAP_IMG_PATH, str_file_name)
                cv.imwrite(str_image_save_path, frame)
                print('Capture saved to ', str_image_save_path)

                captured_frame_base64 = __frame_to_base64__(frame)

        cap.release()

    except Exception as ex:
        message = 'Error occurred while getting frp port:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)

    return captured_frame_base64


def capture_multiple_cameras(lst_cameras):
    """Capture multiple cameras"""
    lst_captured_base64 = []

    for src in lst_cameras:
        cap_img_base64 = capture_camera(src)
        if cap_img_base64 != '':
            lst_captured_base64.append(cap_img_base64)

    return lst_captured_base64


def capture_all_cameras():
    """Capture all available cameras"""
    return capture_multiple_cameras(pcat_config.cap_camera_sources)
