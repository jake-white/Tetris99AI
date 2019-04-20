from PIL import Image
import time
import sys
import serial
from numpy import *
from TetrisAI import get_command
from block import Block, get_block
from desktopmagic.screengrab_win32 import (
	getDisplayRects, saveScreenToBmp, saveRectToBmp, getScreenAsImage,
	getRectAsImage, getDisplaysAsImages)

im = Image.open('reference.png')
pix = im.load()

#init values
startingX = 804
startingY = 123
deltaX = 31
deltaY = 31
startingX += int(deltaX/2)
startingY += int(deltaY/2)

tetrominoQueue = array([
    [
        [1, 1], 
        [1, 1]
    ], 
    [
        [1, 1, 0], 
        [0, 1, 1]
    ], 
    [
        [0, 1, 1], 
        [1, 1, 0]
    ], 
    [
        [1, 1, 1, 1]
    ], 
    [
        [0, 0, 1],
        [1, 1, 1]
    ],
    [
        [1, 0, 0],
        [1, 1, 1]
    ],
    [
        [0, 1, 0],
        [1, 1, 1]
    ]
])


def send_command(serial_connection, command_tuple):
    if(command_tuple[0] != None and command_tuple[1] != None):
        serial_connection.write("{}{}".format(command_tuple[0], command_tuple[1]).encode('ascii'))
        return True
    else:
        return False

def getgamestate():
    px = getRectAsImage((0,0,1920,1080))
    board_state = []
    current_active = None
    for y in range(0, 20):
        board_line = []
        for x in range(0, 10):
            ypos = startingY + int(deltaY*y)
            xpos = startingX + int(deltaX*x)
            #if(y == 2 and x > 2 and x < 7): #in the upper "attackers" zone
                #ypos -= 2
            #elif(y == 3 and x > 2 and x < 7): #in the lower "attackers" zone
                #ypos += 3
            if(y == 19):
                ypos -= 2
            pixelsamples = []
            for i in range(ypos - 7, ypos + 7):
                pixelsamples.append(px.getpixel((xpos, i)))
                px.load()[xpos, i] = (255, 0, 255)
            for j in range(xpos - 7, xpos + 7):
                pixelsamples.append(px.getpixel((j, ypos)))
                px.load()[j, ypos] = (255, 0, 255)
            blocktype = get_block(pixelsamples)
            #if(y < 2 and int(blocktype) < int(Block['ACTIVE_O'])):
                #blocktype = Block['EMPTY']
            if(blocktype >= int(Block['ACTIVE_O'])):
                current_active = int(blocktype)
            if(blocktype == Block['GHOST'] or int(blocktype) >= int(Block['ACTIVE_O']) or blocktype == Block['EMPTY']):
                board_line.append(0)
            else:
                board_line.append(1)
        board_state.append(board_line)

    numpy_board_state = array(board_state)
    if(current_active != None):
        actual_queue = array([tetrominoQueue[current_active]])
        move = get_command(actual_queue, numpy_board_state)[0]
        print("Best move = {}".format(move))
        return move
    else:
        return [None, None]
    

# DO THINGS
time.sleep(1)
ser = serial.Serial('COM3', 9600)
connected = False
waiting = False

while(True):
    if(not connected or waiting):
        connected = True
        waiting = False
        print("Waiting for serial.")
        try:
            val = ser.readline()
        except KeyboardInterrupt:
            # quit
            print("Quitting.")
            sys.exit()
        print("Serial sent {}, continuing program.".format(val))
    if(send_command(ser, getgamestate())):
        waiting = True