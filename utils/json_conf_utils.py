# json_conf_utils.py: Utils for parsing json file and saving conf info to json file
import os
import json


def load_conf(file_path):
    """Load config"""
    conf_json = None

    if os.path.exists(file_path):
        with open(file_path) as file_conf_for_read:
            conf_json = json.load(file_conf_for_read)

    return conf_json


def save_conf(conf_json, file_path):
    """Save the channel config to files"""
    with open(file_path, 'w') as file_conf_for_write:
        json.dump(conf_json, file_conf_for_write)