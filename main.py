from machine import Pin, I2C
import time
import utime
import math
import _thread
from ssd1306 import SSD1306_I2C
import framebuf
import re

# Generated number images by 
# convert -size 32x80 -background '#ffff' -fill black -gravity center label:{number} -resize 32x112! {number}.png
# and to bytearray with https://github.com/novaspirit/img2bytearray/, python3 img2bytearray.py ../{number}.png 32 112 >> barrays.txt
# {number here is the number in question}, arr 0-9
numbers = [
    bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00]\x00\x00\x01\xff\x00\x00\x03\xff\xc0\x00\x07\xff\xe0\x00\x0f\xff\xe0\x00\x0f\xd7\xf0\x00\x1fA\xf0\x00?\x01\xf8\x00>\x00\xf8\x00|\x00\xf8\x00|\x00x\x00\xf8\x00x\x00\xf8\x00|\x00\xf8\x00x\x01\xf0\x00|\x01\xf0\x00|\x01\xe0\x00|\x01\xe0\x00x\x03\xe0\x00|\x03\xe0\x00|\x03\xc0\x00x\x03\xe0\x00|\x07\xc0\x00x\x07\xc0\x00|\x07\xc0\x00x\x07\x80\x00|\x07\xc0\x00x\x07\x80\x00x\x07\x80\x00\xf8\x0f\x80\x00x\x07\x80\x00\xf8\x0f\x80\x00\xf8\x0f\x80\x00\xf8\x07\x80\x00\xf0\x0f\x80\x00\xf0\x0f\x80\x01\xf0\x0f\x00\x01\xf0\x0f\x80\x01\xf0\x0f\x80\x01\xe0\x0f\x00\x03\xe0\x07\x80\x03\xe0\x0f\x80\x03\xe0\x0f\x80\x03\xc0\x07\x80\x07\xc0\x07\x80\x07\x80\x07\xc0\x0f\xc0\x07\xc0\x0f\x80\x07\xc0\x1f\x00\x03\xe0?\x00\x03\xe0~\x00\x03\xfd\xfe\x00\x01\xff\xfc\x00\x01\xff\xf8\x00\x00\xff\xe0\x00\x00?\xd0\x00\x00*\x80\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x80\x00\x00\x1f\x00\x00\x00?\x80\x00\x00\xff\x00\x00\x00\xff\x00\x00\x03\xff\x00\x00\x07\xff\x00\x00\x0f\xfe\x00\x00\x1f\xdf\x00\x00?\x9e\x00\x00\x7f\x1e\x00\x00>>\x00\x008\x1e\x00\x008<\x00\x00\x10>\x00\x00\x00<\x00\x00\x00|\x00\x00\x00<\x00\x00\x00|\x00\x00\x00|\x00\x00\x00x\x00\x00\x00|\x00\x00\x00x\x00\x00\x00\xf8\x00\x00\x00x\x00\x00\x00\xf8\x00\x00\x00\xf8\x00\x00\x00\xf0\x00\x00\x00\xf0\x00\x00\x00\xf0\x00\x00\x01\xf0\x00\x00\x00\xf0\x00\x00\x01\xf0\x00\x00\x01\xf0\x00\x00\x01\xe0\x00\x00\x01\xe0\x00\x00\x01\xe0\x00\x00\x03\xe0\x00\x00\x03\xe0\x00\x00\x03\xe0\x00\x00\x03\xc0\x00\x00\x03\xc0\x00\x00\x03\xc0\x00\x00\x03\xc0\x00\x00\x07\xc0\x00\x00\x07\xc0\x00\x00\x07\xc0\x00\x00\x07\x80\x00\x00\x07\x80\x00\x00\x07\x80\x00\x00\x0f\x80\x00\x00\x07\x80\x00\x00\x0f\x80\x00\x00\x0f\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfc\x00\x00\x03\xff\x80\x00\x0f\xff\xc0\x00\x1f\xff\xc0\x00?\xff\xf0\x00\x7f\x8f\xf0\x00~#\xf0\x00x\x01\xf8\x000\x00\xf8\x00 \x00\xf8\x00\x00\x00x\x00\x00\x00\xf8\x00\x00\x00|\x00\x00\x00x\x00\x00\x00x\x00\x00\x00\xf8\x00\x00\x00x\x00\x00\x00\xf8\x00\x00\x00\xf8\x00\x00\x00\xf0\x00\x00\x01\xf0\x00\x00\x01\xf0\x00\x00\x01\xe0\x00\x00\x03\xe0\x00\x00\x07\xe0\x00\x00\x07\xc0\x00\x00\x0f\x80\x00\x00\x1f\x80\x00\x00\x1f\x00\x00\x00>\x00\x00\x00~\x00\x00\x00\xfc\x00\x00\x00\xf8\x00\x00\x01\xf0\x00\x00\x03\xf0\x00\x00\x07\xe0\x00\x00\x07\xc0\x00\x00\x0f\x80\x00\x00\x1f\x80\x00\x00?\x00\x00\x00~\x00\x00\x00|\x00\x00\x00\xf8\x00\x00\x01\xf8\x00\x00\x03\xe0\x00\x00\x03\xe0\x00\x00\x07\xc0\x00\x00\x0f\x80\x00\x00\x1f\x80\x00\x00?\xbe\xdb@?\xff\xff\x80?\xff\xff\xc0?\xff\xff\x80\x7f\xff\xff\x80?\xff\xff\x80$\x88I\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfc\x00\x00\x07\xff\x80\x00\x1b\xff\xc0\x00/\xff\xe0\x00\x7f\xff\xe0\x00\x7f\x87\xf0\x00\xfc#\xf0\x00x\x01\xf8\x00 \x00\xf8\x00 \x00\xf8\x00\x00\x00x\x00\x00\x00\xf8\x00\x00\x00x\x00\x00\x00x\x00\x00\x00\xf8\x00\x00\x00x\x00\x00\x00\xf8\x00\x00\x00\xf0\x00\x00\x01\xf8\x00\x00\x01\xf0\x00\x00\x03\xe0\x00\x00\x07\xe0\x00\x00\x0b\xc0\x00\x00?\x80\x00\n\xdf\x00\x00\x1f\xfe\x00\x00\x1f\xf8\x00\x00?\xf0\x00\x00\x1f\xf8\x00\x00?\xfe\x00\x00\x00\x7f\x00\x00\x00?\x00\x00\x00\x0f\x80\x00\x00\x0f\x80\x00\x00\x07\xc0\x00\x00\x07\xc0\x00\x00\x07\xc0\x00\x00\x07\xc0\x00\x00\x07\xc0\x00\x00\x03\xc0\x00\x00\x07\xc0\x00\x00\x03\xc0\x00\x00\x07\xc0\x00\x00\x07\xc0\x00\x00\x07\xc0\x00\x00\x0f\x80\x00\x00\x0f\x80 \x00\x1f\x804\x00?\x00<\x00\x7f\x00?\xd5\xfe\x00?\xff\xfc\x00\x1f\xff\xf8\x00\x1f\xff\xf0\x00\x07\xff\xc0\x00\x00\xaa \x00\x00\x11\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf8\x00\x00\x01\xf8\x00\x00\x03\xf8\x00\x00\x03\xf8\x00\x00\x07\xf8\x00\x00\x07\xf0\x00\x00\x0f\xf0\x00\x00\x1e\xf0\x00\x00\x1e\xf0\x00\x00>\xf0\x00\x00<\xf0\x00\x00y\xe0\x00\x00\xf9\xe0\x00\x00\xf1\xe0\x00\x01\xf1\xe0\x00\x01\xe1\xe0\x00\x03\xe3\xe0\x00\x07\xc1\xc0\x00\x07\x83\xe0\x00\x0f\x83\xc0\x00\x0f\x03\xc0\x00\x1f\x03\xc0\x00>\x07\xc0\x00<\x03\xc0\x00|\x07\x80\x00\xf8\x07\xc0\x00\xf0\x07\x80\x01\xf0\x07\x80\x01\xe0\x07\x80\x03\xe0\x0f\x80\x07\xc0\x0f\x80\x07\x80\x0f\x00\x0f\x80\x0f\x00\x0f\x00\x0f\x00\x1f\x00\x0f\x00>\x00\x1f\x00?\xff\xff\xfc?\xff\xff\xfc?\xff\xff\xfc?\xff\xff\xf8\x7f\xff\xff\xf86\xdd\xffx\x00\x00\x1e\x00\x00\x00<\x00\x00\x00>\x00\x00\x00<\x00\x00\x00<\x00\x00\x00<\x00\x00\x00<\x00\x00\x00|\x00\x00\x00x\x00\x00\x00|\x00\x00\x00x\x00\x00\x00x\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\xff\xfc\x00\x0f\xff\xfc\x00\x0f\xff\xf8\x00\x1f\xff\xf8\x00\x1f\xff\xf8\x00\x1fUP\x00\x1e\x00\x00\x00\x1e\x00\x00\x00<\x00\x00\x00>\x00\x00\x00<\x00\x00\x00<\x00\x00\x00<\x00\x00\x00x\x00\x00\x00x\x00\x00\x00x\x00\x00\x00x\x00\x00\x00x\x00\x00\x00\xf0\x00\x00\x00\xf0\x00\x00\x00\xf4\x80\x00\x00\xfb\xf8\x00\x00\xff\xfc\x00\x01\xff\xfe\x00\x01\xff\xff\x00\x00\xfd\xff\x80\x00\xc2?\x80\x00\x00\x0f\xc0\x00\x00\x0f\xc0\x00\x00\x07\xe0\x00\x00\x03\xe0\x00\x00\x03\xe0\x00\x00\x03\xe0\x00\x00\x03\xe0\x00\x00\x01\xe0\x00\x00\x03\xe0\x00\x00\x01\xe0\x00\x00\x03\xe0\x00\x00\x01\xe0\x00\x00\x03\xe0\x00\x00\x03\xe0\x00\x00\x03\xc0\x00\x00\x07\xe0\x00\x00\x07\xc0\x00\x00\x07\xc0\x00\x00\x0f\x80\x10\x00\x1f\x80\x18\x00?\x00\x1e\x00\x7f\x00\x1f\xd5\xfe\x00\x1f\xff\xfc\x00\x1f\xff\xf8\x00\x0f\xff\xf0\x00\x03\xff\xc0\x00\x00\xaa\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\xf8\x00\x00\x1f\xfc\x00\x00\x7f\xfc\x00\x00\xff\xfc\x00\x01\xff\xfc\x00\x03\xfd(\x00\x07\xf2\x00\x00\x0f\xe0\x00\x00\x0f\x80\x00\x00\x1f\x80\x00\x00\x1f\x00\x00\x00>\x00\x00\x00>\x00\x00\x00|\x00\x00\x00x\x00\x00\x00\xf8\x00\x00\x00\xf8\x00\x00\x00\xf0\x00\x00\x01\xf0\x00\x00\x01\xf0\x00\x00\x01\xe0P\x00\x01\xe1|\x00\x03\xe3\xff\x00\x03\xe7\xff\x80\x03\xcf\xff\x80\x03\xdf\xff\xc0\x03\xfe\x0f\xe0\x07\xf8\x03\xe0\x07\xf4\x03\xe0\x07\xf0\x01\xe0\x07\xe0\x01\xf0\x07\xc0\x01\xf0\x07\xc0\x01\xf0\x07\x80\x01\xf0\x07\xc0\x00\xf0\x0f\x80\x01\xf0\x07\x80\x00\xf0\x0f\x80\x01\xf0\x07\x80\x01\xe0\x0f\x80\x01\xf0\x07\x80\x01\xe0\x0f\x80\x01\xe0\x07\x80\x01\xe0\x07\x80\x03\xe0\x07\x80\x03\xc0\x07\xc0\x07\xc0\x07\xc0\x07\xc0\x07\xc0\x0f\x80\x03\xe0\x0f\x80\x03\xf0?\x00\x03\xfd\x7f\x00\x01\xff\xfe\x00\x00\xff\xfc\x00\x00\xff\xf8\x00\x00?\xe0\x00\x00\n\x90\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xff\xff\xfe\x01\xff\xff\xfc\x01\xff\xff\xfc\x01\xff\xff\xfc\x01\xff\xff\xfc\x00\x00\x00\xfc\x00\x00\x00x\x00\x00\x00\xf8\x00\x00\x00\xf0\x00\x00\x01\xf0\x00\x00\x01\xe0\x00\x00\x03\xe0\x00\x00\x03\xe0\x00\x00\x03\xc0\x00\x00\x07\xc0\x00\x00\x07\x80\x00\x00\x0f\x80\x00\x00\x0f\x80\x00\x00\x0f\x00\x00\x00\x1f\x00\x00\x00\x1e\x00\x00\x00>\x00\x00\x00<\x00\x00\x00<\x00\x00\x00|\x00\x00\x00x\x00\x00\x00\xf8\x00\x00\x00\xf0\x00\x00\x00\xf0\x00\x00\x01\xf0\x00\x00\x01\xe0\x00\x00\x03\xe0\x00\x00\x03\xc0\x00\x00\x03\xc0\x00\x00\x07\xc0\x00\x00\x07\x80\x00\x00\x0f\x80\x00\x00\x0f\x00\x00\x00\x1f\x00\x00\x00\x1f\x00\x00\x00\x1e\x00\x00\x00>\x00\x00\x00<\x00\x00\x00|\x00\x00\x00x\x00\x00\x00x\x00\x00\x00\xf8\x00\x00\x00\xf0\x00\x00\x01\xf0\x00\x00\x01\xf0\x00\x00\x03\xe0\x00\x00\x03\xe0\x00\x00\x03\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00^\x00\x00\x01\xff\xc0\x00\x03\xff\xe0\x00\x07\xff\xf0\x00\x0f\xff\xf0\x00\x1f\xd5\xf8\x00\x1fB\xf8\x00?\x00\xfc\x00>\x00|\x00<\x00|\x00|\x00<\x00<\x00|\x00|\x00<\x00x\x00<\x00|\x00|\x00x\x00<\x00<\x00|\x00|\x00x\x00<\x00\xf8\x00>\x00\xf8\x00>\x03\xf0\x00\x1e\x03\xe0\x00\x1f\x8f\xe0\x00\x0f\xbf\x80\x00\x0f\xff\x00\x00\x07\xfd\x00\x00\x07\xfa\x00\x00\x1f\xfc\x00\x00?\xfc\x00\x00~?\x00\x00\xfa\x1f\x00\x01\xf8\x1f\x80\x03\xe0\x07\xc0\x03\xe0\x07\xc0\x07\xc0\x07\xc0\x07\x80\x03\xe0\x0f\x80\x03\xe0\x0f\x80\x01\xe0\x0f\x00\x03\xe0\x0f\x00\x01\xe0\x0f\x00\x01\xe0\x1f\x00\x03\xf0\x0f\x00\x01\xe0\x1f\x00\x03\xe0\x0f\x80\x03\xe0\x0f\x00\x03\xe0\x0f\x80\x07\xc0\x0f\xc0\x07\xc0\x0f\xc0\x0f\xc0\x07\xe0?\x80\x07\xfa\xff\x80\x03\xff\xff\x00\x03\xff\xfe\x00\x00\xff\xf8\x00\x00\x7f\xe8\x00\x00*\xa0\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfa\x00\x00\x03\xfe\x00\x00\x0f\xff\x80\x00\x0f\xff\xc0\x00?\xff\xe0\x00?\x8f\xe0\x00~#\xe0\x00|\x01\xf0\x00\xf8\x01\xf0\x00\xf8\x00\xf0\x01\xf0\x00\xf8\x01\xf0\x00\xf8\x01\xe0\x00x\x03\xe0\x00\xf8\x01\xe0\x00x\x03\xc0\x00x\x03\xe0\x00\xf8\x03\xc0\x00x\x03\xc0\x00x\x03\xc0\x00\xf8\x03\xc0\x00\xf8\x03\xe0\x00\xf8\x03\xc0\x00\xf8\x03\xe0\x01\xf8\x03\xe0\x01\xf0\x03\xe0\x03\xf8\x01\xe0\x07\xf0\x01\xf0\x0b\xf0\x01\xfc/\xf0\x00\xff\xfe\xf0\x00\xff\xfd\xf0\x00\x7f\xf9\xf0\x00?\xf1\xe0\x00\x17\xa1\xe0\x00\x04\x83\xe0\x00\x00\x03\xe0\x00\x00\x03\xe0\x00\x00\x03\xc0\x00\x00\x07\xc0\x00\x00\x07\xc0\x00\x00\x07\x80\x00\x00\x0f\x80\x00\x00\x0f\x80\x00\x00\x0f\x00\x00\x00\x1f\x00\x00\x00?\x00\x00\x00>\x00\x00\x00~\x00\x00\x01\xfc\x00\x08\x02\xf8\x00\x1f\xbf\xf8\x00\x0f\xef\xf0\x00\x1f\xff\xe0\x00\x0f\xff\x80\x00\x0f\xff\x00\x00\x05h\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
]

#Static
class SpeedAlgorithm():
    FIXED_PERIOD = self.FixedPeriod()
    ROLLING_AVERAGE= self.RollingAverage()

    class FixedPeriod:
        def start(self, result_callback, wheel_length, input_line, led):
            self.result_callback = result_callback
            self.wheel_length = wheel_length
            self.input_line = input_line
            self.led = led
            
            # We apply contact cooldown so that multiple touches of the contats during one rotation does not occur
            # Contact cooldown time is set so that it is the highest possible, given the a reasonable max speed of the vehicle:
            # t = d/s, 50mph is around 24m/s, so therefore contact cooldown time = (wheel length (m)) / 24(m/s).
            self.contact_cooldown = wheel_length / 24
            self.second_period = 2 #s
            self.this_period = 0 #s
            self.stopped = False

            # Set an interrupt/event handler for the voltage change, when it contacts 0, voltage will be rising
            self.input_line.irq(trigger=Pin.IRQ_RISING, handler=self.on_lines_contact)
            _thread.start_new_thread(self.second_tick, ())
        

        # We reenable the interrupt so multiple can not trigger at once
        def on_lines_contact(self, pin):
            self.input_line.irq(handler=None)
            self.led.toggle()
            time.sleep(contact_cooldown)
            self.led.toggle()
            self.this_period += 1
            self.input_line.irq(handler=on_lines_contact)
        
        # Main fixed period tick, reports data back to program
        def second_tick(self):
            while not self.stopped:
                calculated_speed = 2.23694 * (self.wheel_length * self.this_period / self.second_period) #m/s -> miles per hour
                self.result_callback(calculated_speed, self.second_period, self.wheel_length) #!!Go back to report the new data to the program!!
                #Reset for next second
                self.this_period = 0
                time.sleep(self.second_period)
            # If stopped, then we terminate this thread, WARNING: I should be using multiprocessing package instead of creating new threads!
            return # hopefully this terminates the thread

        def stop():
            self.stopped = True
            self.input_line.irq(handler=None)
            
    class RollingAverage:
        def start(self, result_callback, wheel_length, input_line, led):
            return
        
        def stop():
            return

class Button:
    def __init__(x, y, oled):
        self.oled = oled
        self.x = x
        self.y = y
        
    def render(self):
        self.oled.rect(x + 0, y + 0, 48, 24, 1)
        self.oled.fill_rect(x + 1, y + 1, 46, 30, 1)
        self.oled.text("ok", x + 44, y + 18)

class App:    
    class BootPage:
        def __init__(self, oled):
            self.oled = oled
            self.current = false
            
        def render(self):
            if not self.current:
                return
            for i in range(96): #bike graphic
                self.oled.fill(0)
                self.oled.text("   __o  ", i * 2 - 64, 44)
                self.oled.text(" _`\<,_ ", i * 2 - 64, 50)
                self.oled.text("(*)/ (*)", i * 2 - 64, 56)
                self.oled.show()
                #self.oled.scroll(i, 0)
            
            for i in range(32): #name
                self.oled.fill(0)
                self.oled.text("Zekiah-A:", 26, (int(i)) - 4)
                self.oled.text("LiteSpeed", 26, (64-int(i)) + 4)
                self.oled.show()
                
            for i in range(128): #swipe transition
                self.oled.line(-128 + i * 2, 64, 0 + i * 2, 0, 0)
                self.oled.show()
                

    class MainPage:
        @property # speed getter, rule of thumb, we always assume speed will be a two digit number, since it is unlikely a bike can go over 99mph
        def speed(self):
            return self._speed
        
        @speed.setter # speed setter
        def speed(self, value):
            self._speed = value
            self.render()
            
        @property #time getter
        def time(self):
            return self._time
        
        @time.setter #time setter
        def time(self, value):
            self._time = value
            self.render()
            
        def __init__(self, oled):
            self._speed = 0
            self._time = 0
            self.oled = oled
            self.current = false
            self.speed_calculate_algorithm = None
            
        def ui_number_converter(self, value, char_index = 0) -> bytearray:
            try:
                # i = (str(value)[char_index] if len(str(value)) - 1 >= char_index else "0")
                return numbers[int(str(value)[char_index])]
            except:
                return numbers[0]

        def calc_algorithm_converter(self, value):
            if not value or value is None:
                return "ERR"
            match = "".join(re.findall("(^[A-Z_]|(?<=[a-z])[A-Z])", value))
            return str(match)
            
        def render(self):
            if not self.current:
                return
            self.oled.fill(0)
            # HUD title
            self.oled.text("LiteSpeed v0.01 - (c) Zekiah", 0, 0)
            self.oled.hline(0, 8, 128, 1)
            self.oled.text(self.calc_algorithm_converter(type(self.speed_calculate_algorithm).__name__), 120, 0) # Current speed calc algorithm used displayer 
            # Main left section
            self.oled.text("Sd:" + str(round(self.speed, 3)), 0, 16) # txt, x, y
            self.oled.hline(0, 28, 64, 2)
            self.oled.text("Tm:" + str(time.localtime(self.time)[4:6])[1:-1].replace(",", ":").replace(" ", ""), 0, 32)
            self.oled.hline(0, 44, 64, 2)
            self.oled.text("Avg: WIP", 0, 48)
            self.oled.hline(0, 60, 64, 2)
            # Main left/right secrion separator
            self.oled.vline(64, 16, 64, 2)
            #Main right section, usable space: 64 * 112
            num1 = framebuf.FrameBuffer(self.ui_number_converter(self.speed), 32, 96, framebuf.MONO_HLSB)
            num2 = framebuf.FrameBuffer(self.ui_number_converter(self.speed, 1), 32, 96, framebuf.MONO_HLSB)
            self.oled.blit(num1, 64, -18, 0) #x,y,key blit draws over cur fb with new
            self.oled.blit(num2, 96, -18, 0)
            self.oled.show()
    
    class StatsPage: #stub
        def __init__(self, oled):
            self.oled = oled
            self.current = false
            
        def render(self):
            if not self.current:
                return
            self.oled.fill(0)
            # Title
            self.oled.text("Litespeed > Stats", 0, 0)
            self.oled.hline(0, 8, 128, 1)
            # Section 1 -> run
            self.oled.text("School run:")
            Button(self.oled, 20, 30)
            # Section separator
            self.oled.vline(96, 16, 64, 1)
            self.oled.show()
    

    def __init__(self, oled):
        self.current_page = None
        self.boot_page = self.BootPage(oled)
        self.main_page = self.MainPage(oled)
        self.stats_page = self.StatsPage(oled)
        self.oled = oled

    def set_current_page(self, page):
        self.current_page = page
        self.current_page.current = true
        self.current_page.render()
        
    def get_current_page(self):
        return self.current_page
    
    def render_current_page(self):
        self.oled.fill(0)
        self.current_page.render()
        self.oled.show()

# Speed = distance / time, we will meassure the speed every second, distance will be the wheel rim diameter
led = Pin(25, Pin.OUT)
output_line = Pin(0, Pin.OUT)
input_line = Pin(1, Pin.IN, Pin.PULL_DOWN)

# Set up display
i2c = I2C(0, sda = Pin(4), scl = Pin(5), freq=400000)
i2c.scan()
utime.sleep(0.1)
oled = SSD1306_I2C(128, 64, i2c)
app = App(oled)
speed_calculate_algorithm = SpeedAlgorithm.FIXED_PERIOD

wheel_diameter = 0.9 #m
wheel_length = math.pi * wheel_diameter #m
speed = 0 #mph
ride_time = 0 #s


def speed_result_callback(speed, period, distance):
    ride_time = ride_time + period
    app.main_page.time = ride_time
    app.main_page.speed = speed


try:
    # Initialise UI
    app.set_current_page(app.boot_page)
    time.sleep(0.1)
    app.set_current_page(app.main_page)

    # All speed calc algorithms require these to be set
    led.value(0)
    output_line.value(1)
    print("started set voltage of 1 on Pin 0\n")

    # Init whatever speed calc algorithm we decide on using
    speed_calculate_algorithm.start(speed_result_callback, wheel_length, input_line, led)
except BaseException as error:    
    print("[FATAL]: Unrecoverable error in program main, please shut down immediately and contact developers!\n" + str(error))
    oled.text("[FATAL] UNRECOVERABLE ERROR:", 0, 0)
    err_formatted = str(error).split("\n")
    for i in range(0, len(err_formatted)):
        oled.text(err_formatted[i], 0, 16 + (16 * i))