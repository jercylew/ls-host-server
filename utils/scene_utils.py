# scene_utils.py: Utils for scene config
import subprocess
import os
import json
import utils.json_conf_utils

MESH_AGENT_CONF_FILE_PATH = '/usr/local/ls-app-deploy-systemd/modbus.json'


def get_scene_name():
    """Get the name of the scene"""
    mesh_agent_conf_path = "/usr/local/ls-app-deploy-systemd/etc/TKTMeshAgent/etc/TKTMeshAgent.json"
    mesh_agent_conf_json = utils.json_conf_utils.load_conf(file_path=mesh_agent_conf_path)

    if mesh_agent_conf_json is None:
        return ""

    resp_scene_name = ""
    try:
        resp_scene_name = mesh_agent_conf_json["scene_name"]
    except Exception as ex:
        message = 'Error occurred while getting scene name:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)

    return resp_scene_name


def set_scene_name(scene_name):
    """Get the name of the scene"""
    old_scene_name = get_scene_name()
    if old_scene_name == scene_name:
        return True, ""

    mesh_agent_conf_path = "/usr/local/ls-app-deploy-systemd/etc/TKTMeshAgent/etc/TKTMeshAgent.json"
    mesh_agent_conf_json = utils.json_conf_utils.load_conf(file_path=mesh_agent_conf_path)
    if mesh_agent_conf_json is None:
        return False, "Failed to set scene name, mesh agent file cannot be opened!"

    message = ""
    result = True
    try:
        mesh_agent_conf_json["scene_name"] = scene_name
        utils.json_conf_utils.save_conf(conf_json=mesh_agent_conf_json, file_path=mesh_agent_conf_path)
    except Exception as ex:
        result = False
        message = 'Error occurred while setting scene name:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)

    return result, message


def get_frp_port():
    """Get the name of the scene"""
    frp_ini_file_path = "/usr/local/frp/frpc.ini"
    if not os.path.exists(frp_ini_file_path):
        return ""

    try:
        frp_port = subprocess.check_output(f"grep remote_port {frp_ini_file_path} | cut -d = -f 2",
                                       shell=True).decode("utf-8")
        frp_port = frp_port.rstrip("\n")
        frp_port = frp_port.lstrip()
    except Exception as ex:
        message = 'Error occurred while getting frp port:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)

    return frp_port


def set_frp_port(frp_port):
    """Get the name of the scene"""
    frp_ini_file_path = "/usr/local/frp/frpc.ini"

    if not os.path.exists(frp_ini_file_path):
        return False, "Frp conf file missing!"

    old_frp_port = get_frp_port()
    if old_frp_port == frp_port:
        return True, ""

    message = ""
    result = True
    try:
        with open(frp_ini_file_path, "w") as frp_ini_save_file:
            frp_ini_save_file.writelines(["[common]", "server_addr = www.lengshuotech.com",
                                          "server_port = 7000", "", f"[ssh-photonicat-{frp_port}]", "type = tcp",
                                          "local_ip = 127.0.0.1", "local_port = 22", f"remote_port = {frp_port}"])
            frp_ini_save_file.flush()

    except Exception as ex:
        result = False
        message = 'Error occurred while setting frp port:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)

    return result, message


def get_scene_address():
    """Get the address of the scene"""
    mesh_agent_conf_path = "/usr/local/ls-app-deploy-systemd/etc/TKTMeshAgent/etc/TKTMeshAgent.json"
    mesh_agent_conf_json = utils.json_conf_utils.load_conf(file_path=mesh_agent_conf_path)

    if mesh_agent_conf_json is None:
        return ""

    resp_scene_address = ""
    try:
        resp_scene_address = mesh_agent_conf_json["scene_address"]
    except Exception as ex:
        message = 'Error occurred while getting scene address:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)

    return resp_scene_address


def set_scene_address(address):
    """Set the address for the scene"""
    old_address = get_scene_address()
    if old_address == address:
        return True, ""

    mesh_agent_conf_path = "/usr/local/ls-app-deploy-systemd/etc/TKTMeshAgent/etc/TKTMeshAgent.json"
    mesh_agent_conf_json = utils.json_conf_utils.load_conf(file_path=mesh_agent_conf_path)
    if mesh_agent_conf_json is None:
        return False, "Failed to set scene address, mesh agent file cannot be opened!"

    message = ""
    result = True
    try:
        mesh_agent_conf_json["scene_address"] = address
        utils.json_conf_utils.save_conf(conf_json=mesh_agent_conf_json, file_path=mesh_agent_conf_path)
    except Exception as ex:
        result = False
        message = 'Error occurred while setting scene address:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)

    return result, message


def get_scene_gps_coordinate():
    """Get the address of the scene"""
    mesh_agent_conf_path = "/usr/local/ls-app-deploy-systemd/etc/TKTMeshAgent/etc/TKTMeshAgent.json"
    mesh_agent_conf_json = utils.json_conf_utils.load_conf(file_path=mesh_agent_conf_path)

    if mesh_agent_conf_json is None:
        return ""

    resp_scene_coordinate = ""
    try:
        resp_scene_coordinate = mesh_agent_conf_json["gps_coordinate"]
    except Exception as ex:
        message = 'Error occurred while getting scene gps coordinate:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)

    return resp_scene_coordinate


def set_scene_coordinate(coordinate):
    """Set the address for the scene"""
    old_coordinate = get_scene_gps_coordinate()
    if old_coordinate == coordinate:
        return True, ""

    mesh_agent_conf_path = "/usr/local/ls-app-deploy-systemd/etc/TKTMeshAgent/etc/TKTMeshAgent.json"
    mesh_agent_conf_json = utils.json_conf_utils.load_conf(file_path=mesh_agent_conf_path)
    if mesh_agent_conf_json is None:
        return False, "Failed to set scene gps coordinate, mesh agent file cannot be opened!"

    message = ""
    result = True
    try:
        mesh_agent_conf_json["gps_coordinate"] = coordinate
        utils.json_conf_utils.save_conf(conf_json=mesh_agent_conf_json, file_path=mesh_agent_conf_path)
    except Exception as ex:
        result = False
        message = 'Error occurred while setting scene gps coordinate:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)

    return result, message


def get_scene_tel_number():
    """Get the address of the scene"""
    mesh_agent_conf_path = "/usr/local/ls-app-deploy-systemd/etc/TKTMeshAgent/etc/TKTMeshAgent.json"
    mesh_agent_conf_json = utils.json_conf_utils.load_conf(file_path=mesh_agent_conf_path)

    if mesh_agent_conf_json is None:
        return ""

    resp_scene_tel_number = ""
    try:
        resp_scene_tel_number = mesh_agent_conf_json["tel_number"]
    except Exception as ex:
        message = 'Error occurred while getting scene telephone number:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)

    return resp_scene_tel_number


def set_scene_tel_number(tel_number):
    """Set the address for the scene"""
    old_tel_number = get_scene_tel_number()
    if old_tel_number == tel_number:
        return True, ""

    mesh_agent_conf_path = "/usr/local/ls-app-deploy-systemd/etc/TKTMeshAgent/etc/TKTMeshAgent.json"
    mesh_agent_conf_json = utils.json_conf_utils.load_conf(file_path=mesh_agent_conf_path)
    if mesh_agent_conf_json is None:
        return False, "Failed to set scene telephone number, mesh agent file cannot be opened!"

    message = ""
    result = True
    try:
        mesh_agent_conf_json["tel_number"] = tel_number
        utils.json_conf_utils.save_conf(conf_json=mesh_agent_conf_json, file_path=mesh_agent_conf_path)
    except Exception as ex:
        result = False
        message = 'Error occurred while setting scene telephone number:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)

    return result, message


def get_scene_camera_channels():
    """Get the address of the scene"""
    camera_channel_conf_path = "/usr/local/ls-app-deploy-systemd/conf.json"
    camera_channel_conf_json = utils.json_conf_utils.load_conf(file_path=camera_channel_conf_path)

    if camera_channel_conf_json is None:
        return []

    resp_channels = []
    try:
        resp_channels = camera_channel_conf_json["channels"]
    except Exception as ex:
        message = 'Error occurred while getting scene camera channels:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)

    return resp_channels


def delete_scene_camera_channel(ch_id):
    """Set the address for the scene"""
    camera_channel_conf_path = "/usr/local/ls-app-deploy-systemd/conf.json"
    camera_channel_conf_json = utils.json_conf_utils.load_conf(file_path=camera_channel_conf_path)
    if camera_channel_conf_json is None:
        return False, "Failed to delete scene camera channel, video server conf file cannot be opened!"

    message = ""
    result = True
    try:

        utils.json_conf_utils.save_conf(conf_json=camera_channel_conf_json, file_path=camera_channel_conf_path)
    except Exception as ex:
        result = False
        message = 'Error occurred while setting scene telephone number:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)

    return result, message


def add_scene_camera_channel(channel_info):
    """Set the address for the scene"""
    old_tel_number = get_scene_tel_number()
    if old_tel_number == tel_number:
        return True, ""

    mesh_agent_conf_path = "/usr/local/ls-app-deploy-systemd/etc/TKTMeshAgent/etc/TKTMeshAgent.json"
    mesh_agent_conf_json = utils.json_conf_utils.load_conf(file_path=mesh_agent_conf_path)
    if mesh_agent_conf_json is None:
        return False, "Failed to set scene telephone number, mesh agent file cannot be opened!"

    message = ""
    result = True
    try:
        mesh_agent_conf_json["tel_number"] = tel_number
        utils.json_conf_utils.save_conf(conf_json=mesh_agent_conf_json, file_path=mesh_agent_conf_path)
    except Exception as ex:
        result = False
        message = 'Error occurred while setting scene telephone number:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)

    return result, message


def update_scene_camera_channel(ch_id, channel_info):
    """Set the address for the scene"""
    old_tel_number = get_scene_tel_number()
    if old_tel_number == tel_number:
        return True, ""

    mesh_agent_conf_path = "/usr/local/ls-app-deploy-systemd/etc/TKTMeshAgent/etc/TKTMeshAgent.json"
    mesh_agent_conf_json = utils.json_conf_utils.load_conf(file_path=mesh_agent_conf_path)
    if mesh_agent_conf_json is None:
        return False, "Failed to set scene telephone number, mesh agent file cannot be opened!"

    message = ""
    result = True
    try:
        mesh_agent_conf_json["tel_number"] = tel_number
        utils.json_conf_utils.save_conf(conf_json=mesh_agent_conf_json, file_path=mesh_agent_conf_path)
    except Exception as ex:
        result = False
        message = 'Error occurred while setting scene telephone number:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)

    return result, message