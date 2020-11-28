from PIL import Image, ImageDraw
from threading import Thread
from time import sleep
import os
from utilities import json_parser
from hashlib import sha256

# util.py is a class used for static methods that are used throughout the project
# Created to keep logic out of main.py

# Used to check if the params are valid
# param - x_value: int between 0 - 500
# param - y_value: int between 0 - 544
# returns: true if params are valid, otherwise false.
def valid_params(x_value, y_value):
    if x_value is None or y_value is None:
        return False
    elif not isinstance(x_value, int) or not isinstance(y_value, int):
        return False
    elif x_value > 500 or y_value > 544:
        return False
    elif x_value < 0 or y_value < 0:
        return False
    else:
        return True

# Method used to create political compass image
# Saves an image as image x_value y_value .png
# param - x_value: int between 0 - 500, where to go on x axis
# param - y_value: int between 0 - 544, where to go on y axis
def manipulate_image(x_value, y_value):
    with Image.open('static/images/compass.jpg') as im:
        draw = ImageDraw.Draw(im)
        draw.regular_polygon((x_value, y_value, 10), 32, fill='#FF0000')
        path = 'static/images/image{0}{1}.png' # Save it as png because JPEG compression is bad.
        formattedPath = path.format(x_value, y_value)
        im.save(formattedPath)

# Starts a thread that deletes the image.
# param - image_path: The path of the image
def delete_image(image_path):
    thread = Thread(target=delete_image_thread, args=(image_path,))
    thread.start()

# Waits x seconds before deleting an image (enough time to load the page)
# param - image_path: The path of the image
def delete_image_thread(image_path):
    sleep(json_parser.image_delete_time())
    os.remove(image_path)

def hash_string(to_hash):
    hash_object = sha256(str.encode(to_hash))
    return_value = hash_object.hexdigest()
    return return_value

def add_question(text, type, sway):
    dict = {
        "question_text":text,
        "type":type,
        "sway":sway
    }
    json_parser.append_question(dict)

    return 0
