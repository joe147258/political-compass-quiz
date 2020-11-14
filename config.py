import json

# This file parses data from config.json.
# This is used to tweek elements without 
# having to relaunch the server.

def config():
    configFile = open("config.json")
    configData = json.load(configFile)
    return configData;

def x_movement():
    return config()["x_movement"]

def y_movement():
    return config()["y_movement"]
 
def delete_time():
    return config()["delete_time"]
