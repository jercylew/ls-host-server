# -*- coding: utf-8 -*-
# @Author    : Qichunren

version = "0.1.6"
skip_auth = False  # Config by --skip-auth, skip linux user password auth. This flag can be changed by other.
web_port = 80  # Config by --port 81
luci_port = 8080

# package_version_url = "https://ao.sh1.xyz:3781/rk3568-photoncat-openwrt/packages-volatile.txt"
package_version_url = "https://dl.photonicat.com/repos/openwrt/packages-volatile.txt"

# volatile_packages_url = "https://ao.sh1.xyz:3781/rk3568-photoncat-openwrt/volatile/"
volatile_packages_url = "https://dl.photonicat.com/repos/openwrt/volatile/"

# video capturing
# Integrals are index of USB connected cameras, also support rtsp sources for IP cameras
# cap_camera_sources = [0, 2, "rtsp://admin:abcd8888@192.168.5.149:554/streaming/channels/402"]
cap_camera_sources = [10, 12]
cap_interval_ms = 500

record_start = False
record_interval_secs = 30
record_camera_sources = [10, 12]
record_camera_frames_qty = 100
record_camera_frames_skip = 1

