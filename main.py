#!/usr/bin/env python3
import videoUpload
import imageUpload
import mediaUpload
import os
import sys
import time
import configparser
import os.path
from os import path

#startup configs/variables
creds = 'credConfig.cfg'
config = configparser.ConfigParser()
config.read(creds)
imageDir = config['misc']['image_dir']
hastags = config['misc']['hastags']
timer = int(config['misc']['timmer'])


starttime = time.time()
#read the last iteration from the file
counterFile = 'counter.txt'
file = open(counterFile, 'r')
file_value = file.read()
file.close()
counter = int(file_value)

def imageList():
    #get an array of the files in the directory
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
    
    
def main(int_counter):
    #create the array of images in the folder
    imageArray = imageList()
    message = 'image: ' + str(int_counter) + hastags
    #upload first image
    mediaUpload.MediaTweet.media_main(imageDir+imageArray[int_counter],message)
    #wait for whatever time you specified in the config file
    time.sleep(timer - ((time.time() - starttime) % timer))
    while True:
        #get the next image
        next_image = newImage(counter,imageArray)
        #construct the test of the tweet
        message = 'image: ' + str(counter) + hastags
        #upload the file
        mediaUpload.MediaTweet.media_main(imageDir+next_image,message)
        #write the current iteration to a file
        file1 = open(counterFile, 'w')
        file1.write(str(counter))
        file1.close()
        #wait for whatever time you specified in the config file
        time.sleep(timer - ((time.time() - starttime) % timer))

    
if __name__ == '__main__':
    main(counter)