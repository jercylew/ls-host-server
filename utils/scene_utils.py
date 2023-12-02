# scene_utils.py: Utils for scene config
import subprocess
import os
import json
import utils.json_conf_utils

MESH_AGENT_CONF_FILE_PATH = '/usr/local/ls-app-deploy-systemd/modbus.json'
CAMERA_VENDOR_HIKVISION = 0
CAMERA_VENDOR_DAHUA = 1


def __get_camera_vendor_from_rtsp__(rtsp):
    """Get the vendor type from the specified rtsp"""
    if "/streaming/channels/" in rtsp:
        return CAMERA_VENDOR_HIKVISION

    if "/cam/realmonitor" in rtsp:
        return CAMERA_VENDOR_DAHUA

    return -1


def __get_rtsp_user__(rtsp):
    """Get the user infor from the rtsp string"""
    # HikVision: rtsp://admin:abcd8888@192.168.5.149:554/streaming/channels/101
    # Dahua: rtsp://admin:y12345678@192.168.2.144:554/cam/realmonitor?channel=2&subtype=1
    if rtsp is None or rtsp == "":
        return "", ""

    user = ""
    password = ""
    camera_vendor = __get_camera_vendor_from_rtsp__(rtsp)
    rtsp = rtsp[7:]
    if camera_vendor == CAMERA_VENDOR_HIKVISION:
        colon_pos = rtsp.index(":")
        at_pos = rtsp.index("@")
        user = rtsp[:colon_pos]
        password = rtsp[colon_pos+1:at_pos]

    if camera_vendor == CAMERA_VENDOR_DAHUA:
        colon_pos = rtsp.index(":")
        at_pos = rtsp.index("@")
        user = rtsp[:colon_pos]
        password = rtsp[colon_pos + 1:at_pos]

    return user, password


def __get_rtsp_ip__(rtsp):
    """Get the IP from the given rtsp"""
    ip = ""
    at_pos = rtsp.index("@")

    if at_pos == -1:
        return ""

    rtsp = rtsp[at_pos+1:]
    colon_pos = rtsp.index(":")
    ip = rtsp[:colon_pos]

    return ip


def __get_rtsp_channel_id__(rtsp):
    """Get the channel ID from given rtsp"""
    channel_id = ""
    camera_vendor = __get_camera_vendor_from_rtsp__(rtsp)

    if camera_vendor < 0:
        return channel_id

    if camera_vendor == CAMERA_VENDOR_HIKVISION:
        last_slash_index = rtsp.rindex("/")
        channel_id = rtsp[last_slash_index+1:]
        zero_index = channel_id.index("0")
        if zero_index >= 0:
            channel_id = channel_id[0:zero_index]

    if camera_vendor == CAMERA_VENDOR_DAHUA:
        start_index = rtsp.index("channel=")
        and_index = rtsp.index("&", start_index+8)
        channel_id = rtsp[start_index+8:and_index]

    return int(channel_id)


def __generate_rtsp_channel_json__(channel_info_json):
    """Generate rtsp for the channel"""
    rtsp_hd = ""
    rtsp_stream = ""

    rtsp_user = channel_info_json["rtsp_user"]
    rtsp_password = channel_info_json["rtsp_password"]
    ip = channel_info_json["rtsp_ip"]
    channel_id = channel_info_json["rtsp_channel_id"]

    if channel_info_json["camera_vendor"] == CAMERA_VENDOR_HIKVISION:
        rtsp_hd = f"rtsp://{rtsp_user}:{rtsp_password}@{ip}:554/streaming/channels/{channel_id}01"
        rtsp_stream = f"rtsp://{rtsp_user}:{rtsp_password}@{ip}:554/streaming/channels/{channel_id}02"
    elif channel_info_json["camera_vendor"] == CAMERA_VENDOR_DAHUA:
        rtsp_hd = f"rtsp://{rtsp_user}:{rtsp_password}@{ip}:554/cam/realmonitor?channel={channel_id}&subtype=1"
        rtsp_stream = f"rtsp://{rtsp_user}:{rtsp_password}@{ip}:554/cam/realmonitor?channel={channel_id}&subtype=2"
    else:
        print("Invalid camera channel info: ", channel_info_json)

    rtsp_channel = {
        "name": channel_info_json["name"],
        "size_video_capture": "1280x720",
        "rtsp_video_upload": rtsp_hd,
        "rtsp_ffmpeg_push": rtsp_stream,
        "rtmp": "",
        "ffmpeg_cmd": "/usr/bin/ffmpeg",
        "ffmpeg_args": "-i $rtsp -vcodec copy -an -f flv $rtmp",
        "ffmpeg_channel_mode": 2
    }

    return rtsp_channel


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
        rtsp_channels = camera_channel_conf_json["channels"]

        for channel in rtsp_channels:
            rtsp = ""
            if "rtsp_video_upload" in channel:
                rtsp = channel["rtsp_video_upload"]
            elif "rtsp_ffmpeg_push" in channel:
                rtsp = channel["rtsp_ffmpeg_push"]
            else:
                print("rtsp not found in channel:", channel)
                continue

            user, password = __get_rtsp_user__(rtsp)
            resp_channel_info = {
                "id": channel["id"],
                "name": channel["name"],
                "camera_vendor": __get_camera_vendor_from_rtsp__(rtsp),
                "rtsp_user": user,
                "rtsp_password": password,
                "rtsp_ip": __get_rtsp_ip__(rtsp),
                "rtsp_channel_id": __get_rtsp_channel_id__(rtsp)
            }
            resp_channels.append(resp_channel_info)

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
        rtsp_channels = camera_channel_conf_json["channels"]
        found_index = -1
        for index in range(0, len(rtsp_channels)):
            if ch_id == rtsp_channels[index]["id"]:
                found_index = index
                break

        if found_index >= 0:
            del rtsp_channels[found_index]

        utils.json_conf_utils.save_conf(conf_json=camera_channel_conf_json, file_path=camera_channel_conf_path)
    except Exception as ex:
        result = False
        message = 'Error occurred while setting scene telephone number:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)

    return result, message


def add_scene_camera_channel(channel_info):
    """Set the address for the scene"""

    camera_channel_conf_path = "/usr/local/ls-app-deploy-systemd/conf.json"
    camera_channel_conf_json = utils.json_conf_utils.load_conf(file_path=camera_channel_conf_path)
    if camera_channel_conf_json is None:
        return False, "Failed to add scene camera channel, video server conf file cannot be opened!"

    message = ""
    result = True
    try:
        rtsp_channels = camera_channel_conf_json["channels"]
        new_channel_json = __generate_rtsp_channel_json__(channel_info)
        new_channel_json["id"] = str(len(rtsp_channels))
        rtsp_channels.append(new_channel_json)

        utils.json_conf_utils.save_conf(conf_json=camera_channel_conf_json, file_path=camera_channel_conf_path)
    except Exception as ex:
        result = False
        message = 'Error occurred while adding new scene camera channel:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)

    return result, message


def update_scene_camera_channel(ch_id, channel_info):
    """Set the address for the scene"""
    camera_channel_conf_path = "/usr/local/ls-app-deploy-systemd/conf.json"
    camera_channel_conf_json = utils.json_conf_utils.load_conf(file_path=camera_channel_conf_path)
    if camera_channel_conf_json is None:
        return False, "Failed to delete scene camera channel, video server conf file cannot be opened!"

    message = ""
    result = True
    try:
        rtsp_channels = camera_channel_conf_json["channels"]
        found_index = -1
        for index in range(0, len(rtsp_channels)):
            if ch_id == rtsp_channels[index]["id"]:
                found_index = index
                break

        new_channel_json = __generate_rtsp_channel_json__(channel_info)
        if found_index >= 0:
            new_channel_json["id"] = rtsp_channels[found_index]["id"]
            del rtsp_channels[found_index]
        else:
            new_channel_json["id"] = str(len(rtsp_channels))

        rtsp_channels.append(new_channel_json)

        utils.json_conf_utils.save_conf(conf_json=camera_channel_conf_json, file_path=camera_channel_conf_path)
    except Exception as ex:
        result = False
        message = 'Error occurred while setting scene telephone number:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)

    return result, message

