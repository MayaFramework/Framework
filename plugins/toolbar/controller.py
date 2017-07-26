import os
import sys
import json
import getpass

CONFIG_PATH = os.path.join(os.getenv("APPDATA"),"MayaToolbar_cfg")

def _config_path():
    if not os.path.isdir(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)
    return CONFIG_PATH

def toolbar_cfg():
    config_path = _config_path()
    toolbar_cfg_path = os.path.join(config_path, "toolbar.json")
    if not os.path.isfile(toolbar_cfg_path):
        default_cfg_file = {"accent_color":"#2196F3", "user_picture":"default_picture.png"}
        with open(toolbar_cfg_path, 'w') as outfile:
            json.dump(default_cfg_file, outfile, indent=4)
    return toolbar_cfg_path

def toolbar_cfg_data():
    toolbar_cfg_path = toolbar_cfg()
    with open(toolbar_cfg_path) as json_data:
        d = json.load(json_data)
    return d

def save_toolbar_cfg_data(data):
    toolbar_cfg_path = toolbar_cfg()
    with open(toolbar_cfg_path, 'w') as f:
        json.dump(data, f)

def current_user():
    return getpass.getuser()

def add_rounded_mask_to_image(image):
    from PIL import Image, ImageOps, ImageDraw, ImageFont
    size = (80, 80)
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0,0) + size, fill=255)
    im = Image.open(image)
    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    save_path = os.path.join(_config_path(), "user_picture.png")
    output.save(save_path)
    print save_path
    return save_path

def create_user_picture():
    from PIL import Image, ImageOps, ImageDraw, ImageFont
    letter = current_user()[0]
    W, H = (100, 100)
    arial = ImageFont.truetype("arial.ttf", 70)
    im = Image.new("RGBA", (W,H))
    draw = ImageDraw.Draw(im)
    draw.ellipse((0,0) + (W,H), outline="#424242", fill="#FAFAFA")
    w,h = arial.getsize(letter)
    draw.text((28,10), letter, font=arial, fill="#2196F3")
    save_path = os.path.join(_config_path(), "default_picture.png")
    im.save(save_path)
    return save_path

# add_rounded_mask_to_image(r"C:\Users\Alberto\Documents\Developements\MayaFramework\Framework\plugins\toolbar\gui\icons\pefil.jpg")