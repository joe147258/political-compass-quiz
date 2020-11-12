from PIL import Image, ImageDraw, ImageFont
# util.py is a class used for static methods that are used throughout the project

# Used to check if the params are valid
# param - x_value: int between 0 - 100
# param - y_value: int between 0 - 100
# returns: true if params are valid, otherwise false.
def valid_params(x_value, y_value):
    if x_value is None or y_value is None:
        return False
    elif not isinstance(x_value, int) or not isinstance(y_value, int):
        return False
    elif x_value > 100 or y_value > 100:
        return False
    elif x_value < 0 or y_value < 0:
        return False
    else:
        return True

# Method used to create an image that shows there standing on the political compass
# param - x_value: int between 0 - 100, where to go on x axis
# param - y_value: int between 0 - 100, where to go on y axix
# returns: an image with their political standing.
# TODO: check out https://pillow.readthedocs.io/en/stable/
def manipulate_image(x_value, y_value):
    img = Image.open('static/images/compass.png')

    # the image to draw in
    draw = ImageDraw.Draw(img)

    # text with new lines
    text = 'HERE\nIS\nSOME\nTEXT'

    # font type (ttf, ttc, etc.) and size - find os path for fonts (will differ on mac vs windows, etc.)
    font = ImageFont.truetype('C:/Users/joe14/Desktop/impact.ttf', 170)

    # draw text on image with xy coordinates
    draw.text((10, 20), text=text, font=font)

    # save a copy of image
    img.save('static/images/image1.png')

    return 0