import pcat_config
import cv2 as cv
import base64
import requests
from datetime import datetime
import time
import os
import threading
from pathlib import Path
# from requests_toolbelt import MultipartEncoder
from multiprocessing import Process
import subprocess

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


def record_camera_video(camera_src, save_path):
    """Record video for the specified camera, and save to a mp4 file"""
    if camera_src < 0 or camera_src == '':
        return ""

    try:
        subprocess.run(f"ffmpeg -f v4l2 -framerate 30 -t 00:00:{pcat_config.record_duration_secs} -i {camera_src} -c:v libx264 -preset ultrafast -crf 23 -pix_fmt yuv420p {save_path}", shell=True)
        print(f"Vide recording done,saved file {save_path}")

    except Exception as ex:
        message = 'Error occurred while record video:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)


def upload_video_to_server(video_file_paths):
    """Upload the specified video to server"""
    server_url = "https://www.shikongteng.com/admin/storage/add"

    for path in video_file_paths:
        if not os.path.exists(path):
            print(f"Video record file {path} not exist, skip it")
            continue

        with open(path, "rb") as file:
            files = {'file': (Path(path).name, file, 'video/mp4')}
            resp = requests.post(server_url, files=files)
            if resp.ok:
                print(f"Upload video file {path} succeed: {resp.text}, {resp} ")
            else:
                print(f"Upload video file {path} failed: {resp.text}")

        if not pcat_config.record_keep_video_file:
            os.remove(path)


def sync_camera_rec_videos():
    """Perform one-time cameras recording and uploading to server"""
    upload_video_files = []
    lst_processes = []

    for camera_src in pcat_config.record_camera_sources:
        print(f"Start recording video from the camera: {camera_src}")
        dt_now = datetime.now()
        str_file_name = 'camera_record_{0}_{1}.mp4'.format(camera_src[-1], dt_now.strftime('%Y%m%d%H%M%S'))
        save_video_path = os.path.join(CAP_IMG_PATH, str_file_name)
        lst_processes.append(Process(target=record_camera_video, args=(camera_src, save_video_path)))

    print('Launch the video recording processes...')
    for i in range(0, len(lst_processes)):
        lst_processes[i].start()
    for j in range(0, len(lst_processes)):
        lst_processes[j].join()

    print('Video recording completed!')
    upload_video_to_server(upload_video_files)


class CameraRecorder(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        # self.board_info = board_info
        # self.tick_count = 0
        # self.network_stats = network_stats.NetworkStats()
        # self.net_download_speed = 0
        # self.net_upload_speed = 0

    def run(self):
        print(f"Camera recorder thread run")
        while True:
            if pcat_config.record_start:
                sync_camera_rec_videos()

            time.sleep(pcat_config.record_interval_secs)

