#@Author    : Qichunren

import spwd, os
import pcat_config

try:
  from passlib.hosts import host_context
except:
  print("Failed to: from passlib.hosts import host_context")

# https://passlib.readthedocs.io/en/stable/lib/passlib.hosts.html
# This function need root permission, so flask app need run as root

def unix_user_auth(user_name, raw_password):
  if pcat_config.skip_auth:
    return True
    
  if user_name is None or raw_password is None:
    return False

  try:
    hash = spwd.getspnam(user_name).sp_pwd
  except Exception as e:
    print("Got error when auth", e)
    return False
  return host_context.verify(raw_password, hash)