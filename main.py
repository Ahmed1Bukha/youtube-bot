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
import requests, base64, random, argparse, os, playsound, time, re, textwrap
TITLE_IMAGE = "title.png"
RIDDLE_IMAGE = "riddle.png"
OUTRO1_IMAGE = "outro1.png"
OUTRO2_IMAGE = "outro2.png"
SESSION_ID = "89c12c43bf1c3f2c6efe9abc0dcf3d03"
VIDEO_PATH = "video/final.mp4"

language = 'en-uk'
introDefult = "Try to solve this riddle!  \n"
newLinerConstant=6
OUTRO1= "Write your answer in the comment below and I will mention the winners in the following video!"
OUTRO2= "Prove that you're smarter than most people"








def convertPartsToVoice(title,riddle,answer):
    

    textToImageMaker(introDefult+title,"title",100)
    textToImageMaker(riddle,"riddle",70)
    textToImageMaker(OUTRO1,"outro1")
    textToImageMaker(OUTRO2,"outro2")
    
    tts(req_text= introDefult+title, filename="voices/intro.mp3")
    


    tts(req_text= riddle, filename="voices/que.mp3")
    
    tts(req_text= "The answer is : "+answer, filename="voices/ans.mp3")
   
    tts(req_text= OUTRO1, filename="voices/outro1.mp3")
    tts(req_text= OUTRO2, filename="voices/outro2.mp3")
  
def textToImageMaker(msg,fileName,size=70):
    
    
    astr = msg
    para = textwrap.wrap(astr, width=28)

    MAX_W, MAX_H = 1080, 1920
    im = Image.new('RGBA', (MAX_W, MAX_H))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype('arial.ttf', size)

    current_h, pad = 850, 5
    for line in para:
        w, h = draw.textsize(line, font=font ,stroke_width=3,)
        draw.text(((MAX_W - w) / 2, current_h), line, font=font,stroke_width=3 , fill=(255,255,255),stroke_fill=(0,0,0))
        current_h += h + pad
    im.save(fileName+".png")

 

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

    totalLenght = wave1+wave2+wave3+wave4
    
    
    # Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60
    clip1 = VideoFileClip(VIDEO_PATH).subclip(0,wave1+0.5)
    clip2 = VideoFileClip(VIDEO_PATH).subclip(wave1+0.5,wave2+1.5)
    clip3 = VideoFileClip(VIDEO_PATH).subclip(wave1+wave2+2.5,wave3+0.5)
    clip4 = VideoFileClip(VIDEO_PATH).subclip(wave1+wave2+wave3+3,wave4+0.5)

    

    # Reduce the audio volume (volume x 0.8)
    clip1 = clip1.volumex(0.8)
    clip2 = clip2.volumex(0.8)
    clip3 = clip3.volumex(0.8)
    clip4 = clip4.volumex(0.8)

    imageClip1= ImageClip(TITLE_IMAGE)
    imageClip1 =imageClip1.set_position('center').set_duration(wave1+0.5)
    
    imageClip2= ImageClip(RIDDLE_IMAGE)
    imageClip2 =imageClip2.set_position('center').set_duration(wave2+1.5)
    
    imageClip3= ImageClip(OUTRO1_IMAGE)
    imageClip3 =imageClip3.set_position('center').set_duration(wave3+0.5)
    
    imageClip4= ImageClip(OUTRO2_IMAGE)
    imageClip4 =imageClip4.set_position('center').set_duration(wave4+0.5)
    
    #Importing voices to the project.
    backgroundMusic =  AudioFileClip("voices/background.mp3")
   
    
    voiceClip1 = AudioFileClip("voices/intro.mp3")
    voiceClip2 = AudioFileClip("voices/que.mp3")
    voiceClip3 = AudioFileClip("voices/outro1.mp3")
    voiceClip4 = AudioFileClip("voices/outro2.mp3")
    
    #Composing the audio together.
    new_audioclip = CompositeAudioClip([backgroundMusic.set_end(2.5+totalLenght),voiceClip1,voiceClip2.set_start(wave1+0.5),voiceClip3.set_start(wave1+wave2+2),voiceClip4.set_start(wave1+wave2+wave3+2.5)])
    
    
    # Overlay the text clip on the first video clip
    video1 = CompositeVideoClip([clip1, imageClip1])
    video2 = CompositeVideoClip([clip2,imageClip2])
    video3 = CompositeVideoClip([clip3,imageClip3])
    video4 = CompositeVideoClip([clip4,imageClip4])
    
    finalVideo = CompositeVideoClip([video1,video2.set_start(wave1+0.5),video3.set_start(wave1+wave2+2),video4.set_start(wave1+wave2+wave3+2.5)])
    
    #Adding the voice together.
    finalVideo.audio = new_audioclip 
    # Write the result to a file (many options available !)
    finalVideo.write_videofile("finalVideoLmfaoi.mp4")
    


def tts(session_id: str = SESSION_ID, text_speaker: str = "en_us_002", req_text: str = "TikTok Text To Speech", filename: str = 'voices/voice.mp3', play: bool = False):

    req_text = req_text.replace("+", "plus")
    req_text = req_text.replace(" ", "+")
    req_text = req_text.replace("&", "and")

    headers = {
        'User-Agent': 'com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)',
        'Cookie': f'sessionid={session_id}'
    }
    url = f"https://api22-normal-c-useast1a.tiktokv.com/media/api/text/speech/invoke/?text_speaker={text_speaker}&req_text={req_text}&speaker_map_type=0&aid=1233"
    r = requests.post(url, headers = headers)

    if r.json()["message"] == "Couldn't load speech. Try again.":
        output_data = {"status": "Session ID is invalid", "status_code": 5}
        print(output_data)
        return output_data

    vstr = [r.json()["data"]["v_str"]][0]
    msg = [r.json()["message"]][0]
    scode = [r.json()["status_code"]][0]
    log = [r.json()["extra"]["log_id"]][0]
    
    dur = [r.json()["data"]["duration"]][0]
    spkr = [r.json()["data"]["speaker"]][0]

    b64d = base64.b64decode(vstr)

    with open(filename, "wb") as out:
        out.write(b64d)

    output_data = {
        "status": msg.capitalize(),
        "status_code": scode,
        "duration": dur,
        "speaker": spkr,
        "log": log
    }

    print(output_data)

    if play is True:
        playsound.playsound(filename)
        os.remove(filename)

    return output_data


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
       
    
    



