import json

# This file parses data from config.json.
# This is used to tweek elements without 
# having to relaunch the server.

def config():
    configFile = open("config.json")
    configData = json.load(configFile)
    return configData

def x_movement():
    return config()["x_movement"]

def y_movement():
    return config()["y_movement"]
 
def image_delete_time():
    return config()["image_delete_time"]

def intro_text():
    return config()["site_info"]["intro_text"]

def admin_config():
    configFile = open("admin_user.json")
    configData = json.load(configFile)
    return configData

def admin_name():
    return admin_config()["username"]
    
def admin_password():
    return admin_config()["password"]
