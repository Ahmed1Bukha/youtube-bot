import requests
import json
import gtts
import os as os
import moviepy.editor as mpy 
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from moviepy.editor import *
from PIL import ImageFont
from tkinter import CENTER
from typing import Sized
from PIL import Image, ImageDraw
from PIL import ImageFont
import textwrap

TITLE_IMAGE = "title.png"
RIDDLE_IMAGE = "riddle.png"
OUTRO1_IMAGE = "outro1.png"
OUTRO2_IMAGE = "outro2.png"

language = 'en-uk'
introDefult = "Can you beat this riddle? try it yourself! the title is : \n"
newLinerConstant=6
OUTRO1= "Write your answer in the comment below!"
OUTRO2= "Don't forget to subscribe so you don't miss the answer in the following video!"



def textToImageMaker(msg,fileName):
    
    
    astr = msg
    para = textwrap.wrap(astr, width=32)

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





def convertPartsToVoice(title,riddle,answer):
    
    textToImageMaker(introDefult+title,"title")
    textToImageMaker(riddle,"riddle")
    textToImageMaker(OUTRO1,"outro1")
    textToImageMaker(OUTRO2,"outro2")
    
  
    introduction = gtts.tts.gTTS(text=introDefult+title ,lang = language)
    introduction.save('voices/intro.mp3')
   
    question = gtts.tts.gTTS(text=riddle,lang = language)
    question.save('voices/que.mp3')
    
    final = gtts.tts.gTTS(text="The answer is : "+answer,lang = language)
    final.save('voices/ans.mp3')
    
    outroVoice1 = gtts.tts.gTTS(text=OUTRO1,lang = language)
    outroVoice1.save('voices/outro1.mp3')
    
    outroVoice2 = gtts.tts.gTTS(text=OUTRO2,lang = language)
    outroVoice2.save('voices/outro2.mp3')


def lengthOfSounds():
    wave1 = MP3("voices/intro.mp3")
    wave2 = MP3("voices/que.mp3")
    wave3 = MP3("voices/outro1.mp3")
    wave4 = MP3("voices/outro2.mp3")
    

    

    wave1 = int(wave1.info.length)
    wave2 = int(wave2.info.length)
    wave3 = int(wave3.info.length)
    wave4 = int(wave4.info.length)
    return wave1,wave2,wave3,wave4   

def makeVideoQuestion():
    wave1,wave2,wave3,wave4 = lengthOfSounds()
    
    
    # Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60
    clip1 = VideoFileClip("3579196.mp4").subclip(0,wave1+0.5)
    clip2 = VideoFileClip("3579196.mp4").subclip(0,wave2+0.5)
    clip3 = VideoFileClip("3579196.mp4").subclip(0,wave3+0.5)
    clip4 = VideoFileClip("3579196.mp4").subclip(0,wave4+0.5)

    

    # Reduce the audio volume (volume x 0.8)
    clip1 = clip1.volumex(0.8)
    clip2 = clip2.volumex(0.8)
    clip3 = clip3.volumex(0.8)
    clip4 = clip4.volumex(0.8)

    imageClip1= ImageClip(TITLE_IMAGE)
    imageClip1 =imageClip1.set_position('center').set_duration(wave1)
    
    imageClip2= ImageClip(RIDDLE_IMAGE)
    imageClip2 =imageClip2.set_position('center').set_duration(wave2+0.5)
    
    imageClip3= ImageClip(OUTRO1_IMAGE)
    imageClip3 =imageClip3.set_position('center').set_duration(wave3+0.5)
    
    imageClip4= ImageClip(OUTRO2_IMAGE)
    imageClip4 =imageClip4.set_position('center').set_duration(wave4+0.5)
    
    #Importing voices to the project.
    voiceClip1 = AudioFileClip("voices/intro.mp3")
    voiceClip2 = AudioFileClip("voices/que.mp3")
    voiceClip3 = AudioFileClip("voices/outro1.mp3")
    voiceClip4 = AudioFileClip("voices/outro2.mp3")
    
    #Composing the audio together.
    new_audioclip = CompositeAudioClip([voiceClip1,voiceClip2.set_start(wave1+0.5),voiceClip3.set_start(wave1+wave2+0.5),voiceClip4.set_start(wave1+wave2+wave3+0.5)])
    
    
    # Overlay the text clip on the first video clip
    video1 = CompositeVideoClip([clip1, imageClip1])
    video2 = CompositeVideoClip([clip2,imageClip2])
    video3 = CompositeVideoClip([clip3,imageClip3])
    video4 = CompositeVideoClip([clip4,imageClip4])
    
    finalVideo = CompositeVideoClip([video1,video2.set_start(wave1+0.5),video3.set_start(wave1+wave2+0.5),video4.set_start(wave1+wave2+wave3+0.5)])
    
    #Adding the voice together.
    finalVideo.audio = new_audioclip
    # Write the result to a file (many options available !)
    finalVideo.write_videofile("finalVideo.mp4")

def main():
    api_url = 'https://api.api-ninjas.com/v1/riddles'
    response = requests.get(api_url, headers={'X-Api-Key': 'D2IzvhY4GK9KbdmvzD9f4Q==1tR0REaKz7lZQzsq'})
    if response.status_code == requests.codes.ok:
        x=str(response.text)
        x=x[1:len(x)-1]
        z=json.loads(x)
        print(z["question"])
        convertPartsToVoice(z["title"],z["question"],z["answer"])
        makeVideoQuestion()
        

    else:
        print("Error:", response.status_code, response.text)


main()
       
    
    



