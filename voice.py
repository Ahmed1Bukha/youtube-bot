from tkinter import CENTER
from typing import Sized
from PIL import Image, ImageDraw
from PIL import ImageFont

newLinerConstant = 6
def newLineMaker(beforeText):
    afterText=""
    beforeText = beforeText.split(" ")
    for i in range(newLinerConstant,len(beforeText), newLinerConstant):
        beforeText.insert(i,"\n")
    for word in beforeText:
        afterText = afterText+ word +" "
    print(afterText)
    return afterText


def textToImageMaker(msg,fileName):
    
    
    astr = msg
    para = textwrap.wrap(astr, width=30)

    MAX_W, MAX_H = 1080, 1920
    im = Image.new('RGBA', (MAX_W, MAX_H))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype('arial.ttf', 50)

    current_h, pad = 850, 5
    for line in para:
        w, h = draw.textsize(line, font=font)
        draw.text(((MAX_W - w) / 2, current_h), line, font=font)
        current_h += h + pad
    im.save(fileName+".png")


    
from PIL import Image, ImageDraw, ImageFont
import textwrap

astr = 'Lorem ipsum dolor sit amet, consectetur adipiscing  Donec at tellus diam. Proin id rutrum nibh.'
para = textwrap.wrap(astr, width=30)

MAX_W, MAX_H = 1080, 1920
im = Image.new('RGBA', (MAX_W, MAX_H))
draw = ImageDraw.Draw(im)
font = ImageFont.truetype('arial.ttf', 50)

current_h, pad = 850, 5
for line in para:
    w, h = draw.textsize(line, font=font)
    draw.text(((MAX_W - w) / 2, current_h), line, font=font)
    current_h += h + pad

im.save('test.png')