import time
import struct
import numpy as np
import pyautogui
import cv2
import pyscreenshot as ImageGrab
import mss
import mss.tools
#import Quartz.CoreGraphics as CG
import os
#import actionCNN as myNN

from pynput import keyboard

#import actionCNN as myNN
import time
import threading

from test2 import MyClass as mc

x=662
y=360
width=200
height=120
mon = (x, y, x+width,y+height)
monitor = {'top': y, 'left': x, 'width': width, 'height': height}
output = 'jump';
img=np.asarray([]);

def get_image(im):
    return im.crop(mon)

def listen():
    listener = keyboard.Listener(on_press = on_press,on_release = on_release)
    listener.start()

# Globals
isEscape = False
saveImg = False
counter1 = 0
counter2 = 0
banner =  '''\nWhat would you like to do ?
    1- Use pretrained model for gesture recognition & layer visualization
    2- Train the model (you will require image samples for training under .\imgfolder)
    3- Generate training image samples. Note: You need to be in 'sudo' i.e admin mode.
    '''

def SaveInImages2(output,cnt,sct_img):
    im = pyautogui.screenshot(region=(x, y, 180,125))
    print(type(im))
    im.save('imgfolder2/'+output+str(cnt)+'.png')
    cnt=cnt+1
    return cnt
    '''with mss.mss() as sct:
        print "ger"
        sct_img=img
        #monitor = {'top': y, 'left': x, 'width': 135, 'height': 125}
        #sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output='imgfolder2/'+output+str(cnt)+'.png')
        print 'imgfolder2/'+output+str(cnt)+'.png'
        cnt=cnt+1
    return cnt'''


# This function gets called when user presses any keyboard key
def on_press(key):
    global isEscape, saveImg, sp, counter1, counter2,monitor,output,img
    
    # Pressing 'UP arrow key' will initiate saving provided capture region images
    if key == keyboard.Key.up:
        saveImg = True
        counter1=SaveInImages2("jump",counter1,img)
        print("done")

    if key == keyboard.Key.down:
        saveImg = True
        counter2=SaveInImages2("nojump",counter2,img)
        print("done")

# This function gets called when user releases the keyboard key previously pressed
def on_release(key):
    global isEscape, saveImg, sp, counter1
    if key == keyboard.Key.esc:
        isEscape = True
        # Stop listener
        return False

def listen():
    listener = keyboard.Listener(on_press = on_press,on_release = on_release)
    listener.start()


def kbAction(key):
    if key == 0:
        jump = ''' osascript -e 'tell application "System Events" to key code 126' '''
        os.system(jump)


def main():
    global isEscape, saveImg, sp, counter2,img
 
    guess = False
    lastAction = -1
    mod = 0
    
    #listen()

    
    #Call CNN model loading callback
    while True:
        ans = int(input( banner))
        #ans=3
        if ans == 1:
            mc.pre_execute()
            while True:
                with mss.mss() as sct:
                    #sct.shot(mon)
                    img = np.asarray(sct.grab(mon))
                    cv2.imshow("sdsd", img)
                    pp=mc.mypredict(img)
                    if(pp==[0]):
                        print("jump")
                    else:
                        print("nojump")
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                        break
            break
        elif ans == 2:
            mod = myNN.loadCNN(-1)
            myNN.trainModel(mod)
            input("Press any key to continue")
            break
        elif ans == 3:
            listen()
            while True:
                # The simplest use, save a screen shot of the 1st monitor
                with mss.mss() as sct:
                    #sct.shot(mon)
                    img = np.asarray(sct.grab(mon))
                    cv2.imshow("sdsd", img)
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                        break
            break
        else:
            print("Get out of here!!!")
            return 0

main()

