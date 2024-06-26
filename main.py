#!/usr/bin/env python3

# @Author    : Qichunren

# NOTE: Not edit pcat-manager-web-main.py, edit main.py instead.

import os
import sys
import pathlib
import getopt
# import pyprctl # patch:set real thread name
import pcat_config
from pcat_manager_web import FlaskAppThread
from pc_socket_client import PcSocketClient
import app
import utils.camera_utils
import utils.json_conf_utils
from pathlib import Path


def load_config():
    """Load settings from config.json file"""
    conf_path = os.path.join(Path(__file__).resolve().parent, 'conf.json')
    conf_json = utils.json_conf_utils.load_conf(file_path=conf_path)

    if conf_json is None:
        return

    try:
        pcat_config.record_start = conf_json["record_start"]
        pcat_config.record_keep_video_file = conf_json["record_keep_video_file"]
        pcat_config.record_camera_sources = conf_json["record_camera_sources"]
        pcat_config.record_interval_secs = conf_json["record_interval_secs"]
        pcat_config.record_duration_secs = conf_json["record_duration_secs"]
    except Exception as ex:
        message = 'Error occurred while getting host id:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)


if __name__ == "__main__":
    current_working_path = pathlib.Path(__file__).parent.resolve()
    os.chdir(str(current_working_path))

    argv = sys.argv[1:]

    # Load config from config.json file
    load_config()

    # The options from command line can override the ones from config.json file
    try:
        opts, args = getopt.getopt(argv, "hvp:", ["port=", "version", "help", "skip-auth"])
    except getopt.GetoptError as error_msg:
        print('main.py got commandline arg error:', error_msg)
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-v" or opt == "--version":
            print(pcat_config.version)
            sys.exit(0)
        elif opt == "-h" or opt == "--help":
            help_doc = """
photonicat web interface tool, v{version}
Listen on http://0.0.0.0:{port} 
      """.strip()
            print(help_doc.format(version=pcat_config.version, port=pcat_config.web_port))
            sys.exit(0)
        elif opt == "-p" or opt == "--port":
            print("Config web port to", arg)
            pcat_config.web_port = int(arg)
        elif opt == "--skip-auth":
            print("skip-auth flag enabled.")
            pcat_config.skip_auth = True

    # python3 ./main.py -v -h --skip-auth arg1 arg2
    # opts: [('-v', ''), ('-h', ''), ('--skip-auth', '')]
    # args: ['arg1', 'arg2']
    #
    # python3 ./main.py arg0 -h --skip-auth arg1 arg2
    # opts: []
    # args: ['arg0', '-h', '--skip-auth', 'arg1', 'arg2']

    # socket_client_obj = PcSocketClient()
    # app.socket_client = socket_client_obj
    # socket_client_obj.start()

    flask_web_thread = FlaskAppThread()
    app.flask_app = flask_web_thread
    flask_web_thread.start()

    main_app = app.App()
    app.main_app = main_app
    main_app.start()

    camera_recorder = utils.camera_utils.CameraRecorder()
    camera_recorder.start()
