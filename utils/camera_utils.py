import pcat_config
import cv2 as cv
import base64
import requests
from datetime import datetime
import time
import os
import threading
from pathlib import Path

CAP_IMG_PATH = os.path.join(Path(__file__).resolve().parent, '../captures')


def __frame_to_base64__(frame):
    """Convert a opencv captured frame(numpy array) to base64 string"""
    retval, buffer = cv.imencode('.jpg', frame)
    base64_txt = str(base64.b64encode(buffer), encoding='utf-8')
    return base64_txt


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


def record_camera_video(camera_src):
    """Record video for the specified camera, and save to a mp4 file"""
    if camera_src < 0 or camera_src == '':
        return ""

    save_video_path = ""
    try:
        cap = cv.VideoCapture(camera_src)
        if cap.isOpened():
            print('Begin recording...')
            dt_now = datetime.now()
            str_file_name = '{0}.mp4'.format(dt_now.strftime('%Y%m%d%H%M%S'))
            save_video_path = os.path.join(CAP_IMG_PATH, str_file_name)

            fourcc = cv.VideoWriter_fourcc(*'MP4V')
            frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
            out = cv.VideoWriter(save_video_path, fourcc, 20.0, (frame_width, frame_height))

            frame_write_counts = 0
            frame_sample_counts = 0

            while frame_write_counts < pcat_config.record_camera_frames_qty:
                ret, frame = cap.read()

                if ret:
                    frame_sample_counts += 1
                    if frame_sample_counts > pcat_config.record_camera_frames_skip:
                        out.write(frame)
                        frame_sample_counts = 0
                        frame_write_counts += 1

            out.release()

        cap.release()

    except Exception as ex:
        message = 'Error occurred while record video:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)
        save_video_path = ""

    return save_video_path


def upload_video_to_server(video_file_path):
    """Upload the specified video to server"""
    server_url = "https://www.shikongteng.com/admin/storage/add"
    # upload_files = {}
    #
    # for path in video_file_paths:
    #     file_name = Path(path).name
    #     upload_files[file_name] = open(path)
    #
    # resp = requests.post(server_url, files=upload_files)
    # if resp.ok:
    #     print(f"Upload video file {video_file_paths} succeed!")
    # else:
    #     print(f"Upload video file {video_file_paths} failed!")
    headers = {
        'Content-Type': 'video/mp4'
    }

    with open(video_file_path, "rb") as file:
        file_data = file.read()
        resp = requests.post(server_url, data=file_data, headers=headers)
        if resp.ok:
            print(f"Upload video file {video_file_path} succeed!")
        else:
            print(f"Upload video file {video_file_path} failed: {resp.text}")


class CameraRecorder(threading.Thread):

    def __init__(self, camera_src):
        threading.Thread.__init__(self)

        # self.board_info = board_info
        # self.tick_count = 0
        # self.network_stats = network_stats.NetworkStats()
        # self.net_download_speed = 0
        # self.net_upload_speed = 0
        self.camera_src = camera_src

    def run(self):
        print(f"Camera recorder thread run, camera source: {self.camera_src}")
        while True:
            if pcat_config.record_start:
                print(f"Start recording video from the camera: {self.camera_src}")
                rec_video_file_path = record_camera_video(self.camera_src)
                if os.path.exists(rec_video_file_path):
                    upload_video_to_server(rec_video_file_path)

            time.sleep(pcat_config.record_interval_secs)

