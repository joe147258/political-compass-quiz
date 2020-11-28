import json

# This file parses data from config.json.
# This is used to tweek elements without 
# having to relaunch the server.

def config():
    file = open('json/config.json')
    data = json.load(file)
    return data

def site_data():
    file = open('json/site_data.json')
    data = json.load(file)
    return data

def question_data():
    file = open('json/question_data.json')
    data = json.load(file)
    return data

def admin_config():
    file = open('json/admin_user.json')
    data = json.load(file)
    return data

def append_question(dict):
    data = question_data()
    data['question_list'].append(dict)
    with open('json/question_data.json', 'w') as fp:
        json.dump(data, fp)

def x_movement():
    return config()['x_movement']

def y_movement():
    return config()['y_movement']
 
def image_delete_time():
    return config()['image_delete_time']

def intro_text():
    return site_data()['intro_text']

def question_list():
    return question_data()['question_list']

def admin_name():
    return admin_config()['username']
    
def admin_password():
    return admin_config()['password']
