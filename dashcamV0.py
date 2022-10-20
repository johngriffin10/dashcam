import datetime
import time
import os
import numpy as np
import sys
import colorsys
import cv2 as cv
import urllib
import subprocess
import platform
from io import BytesIO

PC = 1
cpuType = platform.processor()
if len(cpuType) < 2:
    PC = 0
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    import picamera
    import picamera.array


hz = 5  # frequency in hz that data will be saved
freqWrite = 1 / hz

# __________________________CAMERA___SETUP______________________________________________________________
# cameraName = 'piCam1' #name of camera and path of where its image data is
nocamera = 0  # false if camera is present
h = 720
w = 1280
try:  # try to use camera
    camera = picamera.PiCamera()
    camera.resolution = (h, w)
except:  # if error is thrown IE: no camera installed
    print('no camera detected')
    nocamera = 1  # true if no camera present


# get WiFi time/date and create save location________________________________________________________________________________________________________
timeOut = 60  # wait X seconds to receive GPS time
timeNow = 0
tic = time.time()
synced = 0

while (timeNow < timeOut and synced != 1):  # run until timed out
    timeNow = time.time() - tic
    ps = subprocess.Popen(['iwconfig'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        output = subprocess.check_output(('grep', 'ESSID'), stdin=ps.stdout)
        status = "Connected"
        print("wireless network connected")
        synced = 1
    except subprocess.CalledProcessError:
        # grep did not match any lines
        print("No wireless networks connected")
        status = "NotConnected"

    if status == "Connected":
        date = datetime.datetime.now()  # get date now

if (synced == 0):
    print('WiFi clock not synced... using date/time from PI')
    date = datetime.datetime.now()  # get date now
    print(date, flush=True)  # print date/time from PI

DateFLDR0 = date.strftime("0_0_0")
#DateTime = date.strftime("%H_%M_%S___date_%Y_%m_%d")
DirectoryBase = '//home//pi//Documents//Dashcam//'

def captureVideo(DateTimeNow):
    camera.start_recording(DirectoryBase + DateFLDR0 + DateTimeNow + '.h264')
    print('rec')
    camera.wait_recording(2)
    camera.stop_recording()

#start taking video________________________________________________________________________________________________________
while(1==1): #could make this only capture at night with openCV
    DTime = date.strftime("%H_%M_%S_")
    DateFLDR1 = date.strftime("%Y_%m_%d//")
    if DateFLDR0 != DateFLDR1:
        DateFLDR0 = date.strftime("%Y_%m_%d//")
        DirectoryBase = '//home//pi//Documents//Dashcam//'
        Directory_date = DirectoryBase + DateFLDR0  # make folder for this time
        try:
            os.mkdir(Directory_date)
        except OSError as error:
            #print(error)  # say what went wrong with making the new folders
            Directory_date = Directory_date
    print('capt')
    captureVideo(DTime)
    camera.capture(DirectoryBase + DateFLDR0 + DTime+'.jpg')
    exit()




