#!/usr/bin/env python3
import videoUpload
import imageUpload
import os
import sys
import time
import configparser
import os.path
from os import path

hastags = '\n\r #prfm #perfume_um #kashiyuka #ksyk #かしゆか'
imageDir =''
starttime = time.time()

counterFile = 'counter.txt'
file = open(counterFile, 'r')
file_value = file.read()
file.close()
counter = int(file_value)
def imageList():
    imageArray = os.listdir(imageDir)
    return imageArray
    
def newImage(int_counter,imageArray):
    #see if we are at the end of the array
    #if we are, first check if new files were added
    #if not, go back to 0
    if len(imageArray) <= int_counter+1:
        imageArray = imageList()
        if len(imageArray) == int_counter+1:
            int_counter = 0
        else:
            int_counter = int_counter+1
    else:
        int_counter = int_counter+1
    global counter
    counter = int_counter
    next_image = imageArray[counter]
    #make sure the file exists
    #if the file doesnt exist, it means the folder needs to be rescanned
    #and the array will start back at 0
    if path.exists(imageDir+next_image):
        print("file exists")
    else:
        next_image = imageArray[0]
    return next_image
    
    
def upload(filename,message):
    if filename.endswith(".mp4"):
        videoUpload.VideoTweet.video_main(filename,message)
    else:
        imageUpload.ImageTweet.image_main(filename,message)


def main(int_counter):
    config = configparser.ConfigParser()
    config.read(creds)
    global imageDir 
    imageDir = config['misc']['image_dir']
    imageArray = imageList()
    message = 'image: ' + str(int_counter) + hastags
    upload(imageDir+imageArray[int_counter],message)
    time.sleep(1200.0 - ((time.time() - starttime) % 1200.0))
    while True:
        next_image = newImage(counter,imageArray)
        message = 'image: ' + str(counter) + hastags
        upload(imageDir+next_image,message)
        file1 = open(counterFile, 'w')
        file1.write(str(counter))
        file1.close()
        time.sleep(1200.0 - ((time.time() - starttime) % 1200.0))

    
if __name__ == '__main__':
    creds = 'credConfig.cfg'
    main(counter)