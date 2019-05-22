#!/usr/bin/env python

import threading, time, opc, serial, cv2, random
from playsound import playsound

client = opc.Client('127.0.0.1:7890')
# client = opc.Client('127.0.0.1:22368')
numLEDs = 60
pixels = [(0, 0, 0)] * numLEDs
pixel_off = (0, 0, 0)
pixel_red = (255, 0, 0)
animation_speed = 1
colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0), (255, 0, 255), (255, 165, 0)]


def play_animation():
    global pixels
    global client
    global numLEDs
    global pixel_off
    global pixel_red
    global animation_speed

    for x in range(16):
        pixels = [random.choice(colors)] * numLEDs
        client.put_pixels(pixels)
        time.sleep(animation_speed)
        pixels = [pixel_off] * numLEDs
        client.put_pixels(pixels)
        time.sleep(animation_speed)

try:
    serial_port = serial.Serial('/dev/ttyUSB1', 9600)
except:
    serial_port = serial.Serial('/dev/ttyUSB0', 9600)
sound = "Louis_Graduation.mp3"
button_error = False

while True:
    try:
        if button_error == True:
            try:
                serial_port = serial.Serial('/dev/ttyUSB1', 9600)
                button_error = False
            except:
                try:
                    serial_port = serial.Serial('/dev/ttyUSB0', 9600)
                    button_error = False
                except:
                    button_error = True
        button_status = serial_port.readline().decode().strip('\r\n')
    except:
        print("button error")
        button_error = True
        time.sleep(300)
        pass
    # print(button_status)
    if (button_status == '1'):
        t = threading.Thread(target=play_animation)
        t.daemon = True
        t.start()
        try:
            playsound(sound)
        except:
            print("Can't play audio")
        try:
            serial_port.reset_input_buffer()
        except:
            pass