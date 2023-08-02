# host_utils.py: Utils for host config
import subprocess
import utils.json_conf_utils
import os
import json

MESH_AGENT_CONF_FILE_PATH = '/usr/local/ls-app-deploy-systemd/modbus.json'


def get_host_name():
    """Get the host name of the system"""
    resp_host_name = subprocess.check_output("hostname",
                                              shell=True).decode("utf-8")
    resp_host_name = resp_host_name.rstrip("\n")

    return resp_host_name


def set_host_name(host_name):
    """Set host name """
    old_host_name = get_host_name()
    if host_name == old_host_name:
        return True, ""

    subprocess.run(f"hostnamectl set-hostname {host_name}", shell=True)
    subprocess.run(f"sed -i 's/{old_host_name}/{host_name}/g' /etc/hosts", shell=True)
    return True, ""


def get_host_id():
    """Get the host ID of the system"""
    mesh_agent_conf_path = "/usr/local/ls-app-deploy-systemd/etc/TKTMeshAgent/etc/TKTMeshAgent.json"
    mesh_agent_conf_json = utils.json_conf_utils.load_conf(file_path=mesh_agent_conf_path)

    if mesh_agent_conf_json is None:
        return ""

    resp_host_id = ""
    try:
        host_conf_json = mesh_agent_conf_json["host_info"]
        resp_host_id = host_conf_json["host_id"]
    except Exception as ex:
        message = 'Error occurred while getting host id:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)

    return resp_host_id


def set_host_id(host_id):
    """Set the host id"""
    mesh_agent_conf_path = "/usr/local/ls-app-deploy-systemd/etc/TKTMeshAgent/etc/TKTMeshAgent.json"
    mesh_agent_conf_json = utils.json_conf_utils.load_conf(file_path=mesh_agent_conf_path)

    if mesh_agent_conf_json is None:
        return False, "Mesh agent conf file missing!"

    old_host_id = get_host_id()
    if old_host_id == host_id:
        return True, ""

    message = ""
    result = True
    try:
        host_conf_json = mesh_agent_conf_json["host_info"]
        host_conf_json["host_id"] = host_id
        utils.json_conf_utils.save_conf(conf_json=mesh_agent_conf_json, file_path=mesh_agent_conf_path)
    except Exception as ex:
        message = 'Error occurred while setting host id:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)
        result = False

    return result, message


def get_host_key():
    resp_host_key = ""
    mesh_agent_conf_path = "/usr/local/ls-app-deploy-systemd/etc/TKTMeshAgent/etc/TKTMeshAgent.json"
    mesh_agent_conf_json = utils.json_conf_utils.load_conf(file_path=mesh_agent_conf_path)

    if mesh_agent_conf_json is None:
        return ""

    resp_host_key = ""
    try:
        host_conf_json = mesh_agent_conf_json["host_info"]
        resp_host_key = host_conf_json["host_key"]
    except Exception as ex:
        message = 'Error occurred while getting host id:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)

    return resp_host_key


def set_host_key(host_key):
    """Set the host key"""
    mesh_agent_conf_path = "/usr/local/ls-app-deploy-systemd/etc/TKTMeshAgent/etc/TKTMeshAgent.json"
    mesh_agent_conf_json = utils.json_conf_utils.load_conf(file_path=mesh_agent_conf_path)

    if mesh_agent_conf_json is None:
        return False, "Mesh agent conf file missing!"

    old_host_key = get_host_key()
    if old_host_key == host_key:
        return True, ""

    message = ""
    result = True
    try:
        host_conf_json = mesh_agent_conf_json["host_info"]
        host_conf_json["host_key"] = host_key
        utils.json_conf_utils.save_conf(conf_json=mesh_agent_conf_json, file_path=mesh_agent_conf_path)

    except Exception as ex:
        message = 'Error occurred while getting host id:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)
        result = False

    return result, message

