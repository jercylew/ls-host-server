#!/usr/bin/env python3

import shutil
import pathlib
import sys
import os
import subprocess
import requests

## Install from a remote url
# Steps:
# 1. Get package file from somewhere.
# 2. Unpack downloaded file.
# 3. Find all ipk files in unpacked directory.
# 4. Invoke `opkg install /xx/xx/a.ipk /xx/xx/b.ipk /xx/xx/c.ipk /xx/xx/d.ipk /xx/xx/e.ipk`
# tar.gz, tar.xz,  tar.bz2, *.tar
# tar -xzf xxx.tar.gz
# tar -xjf xxx.tar.bz2
# tar -xJf xxx.tar.xz
# tar -xf xxx.tar
# with open("/cmd-shell/cmd-log.txt","wb") as out, open("/cmd-shell/cmd-log.txt","wb") as err:
### subprocess.run(["/usr/bin/opkg-install.py", "install", "/cmd-shell/a.tar.xz"], stdout=out,stderr=err)


workspace = "/cmd-shell"

if len(sys.argv) < 2:
  print("Missing cmd argument! Available cmd: install")
  exit(1)

if sys.argv[1] != "install":
  print("Not support cmd '{}'".format(sys.argv[1]))
  exit(1)

if sys.argv[1] == "install":
  if len(sys.argv) < 3:
    print("Missing file argument!")
    exit(1)

  try:
    pathlib.Path(workspace + "/out").mkdir(parents=True, exist_ok=True)
  except:
    print("Failed to create dir in {}".format(workspace))
    exit(2)
  os.chdir(workspace)
  print("Current working dir {}".format(os.getcwd()))
  filename = sys.argv[2]
  if filename.startswith("http"):
    try:
      print("Start downloading " + filename)
      r = requests.get(filename, allow_redirects=True)
      print("Download result: " + str(r.status_code))
    except:
      print("Failed to download")
      exit(2)

    current_working_path = pathlib.Path(__file__).parent.resolve()
    base_file_name = os.path.basename(filename)
    save_dir_path = current_working_path.joinpath("temp")
    save_file_path = current_working_path.joinpath("temp", base_file_name)
    try:
      pathlib.Path(save_dir_path).mkdir(parents=True, exist_ok=True)
    except:
      print("Failed to create temp dir")
      exit(3)

    open(save_file_path, 'wb').write(r.content)
    filename = str(save_file_path)
    print("File downloaded.")

  file_exists = os.path.exists(filename)
  if not file_exists:
    print("File '{}' not found!".format(filename))
    exit(2)

  shutil.rmtree('out', ignore_errors=True)
  
  file_size = os.path.getsize(filename) / 1024.0 / 1024.0
  print("File size {} M".format(round(file_size, 2)))
  if file_size > 200.0:
    print("Not support upload file size large than 200 M")
    exit(3)

  if filename.endswith(".ipk"):
    print("Install ipk file")
    cmd = ["opkg", "install", filename]
    print(cmd)
    subprocess.run(cmd)
    print("ipk installed success.")
  elif filename.endswith(".gz") or filename.endswith(".xz") or filename.endswith(".bz2") or filename.endswith(".tar"):
    print("Process archive file ...")
    shutil.rmtree('out', ignore_errors=True)
    extract_dir = "out"
    shutil.unpack_archive(filename, extract_dir)
    result = list(pathlib.Path(extract_dir).rglob("*.ipk"))
    files = [os.getcwd() + "/" + str(file_path) for file_path in result]
    #print("Install files {}".format(files))
    cmd = ["opkg", "install"]
    cmd.extend(files)
    print(cmd)
    subprocess.run(cmd)
    try:
      print("Clean temp files ...")
      shutil.rmtree(workspace, ignore_errors=True)
    except:
      print("Failed to clean extracted files")
    try:
      print("Remove", filename)
      os.remove(filename)
    except:
      print("Failed to remove", filename)
    print("Finished")
  else:
    print("Not support file format!")
    exit(4)