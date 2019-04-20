from enum import Enum
Block = {
    'UNKNOWN':-4,
    'EMPTY':-3,
    'GHOST':-2,
    'INACTIVE':-1,
    'ACTIVE_O':0,
    'ACTIVE_Z':1,
    'ACTIVE_S':2,
    'ACTIVE_I':3,
    'ACTIVE_L':4,
    'ACTIVE_J':5,
    'ACTIVE_T':6
}

#known colors
emptyColor = [9,9,9]
textColor = [85,89,88]
garbage =  [115,121,119]
#o, z, s, i, l, j, t
strings = ["ACTIVE_O", "ACTIVE_Z", "ACTIVE_S","ACTIVE_I","ACTIVE_L","ACTIVE_J","ACTIVE_T"]
ghosts = [[77,66,0], [94,0,21], [17,92,0], [0,79,79], [51,16,0], [10,8,71], [39,0,71]]
active = [[211,190,0], [206,0,53], [78,247,0], [0,222,225], [209,74,0], [37,26,251], [151,0,252]]
blocks= [[127,115,0], [140,0,36], [40,151,0], [0,137,135], [128,38,0], [23,19,167], [99,0,167]]


def color_distance(color, nextcolor): #get distance between 2 colors
    distance = abs(color[0] - nextcolor[0]) + abs(color[1] - nextcolor[1]) + abs(color[2] - nextcolor[2])
    return distance

def get_block(samples):
    blocktype = Block['UNKNOWN']
    for sample in samples:
        for color in ghosts:
            if(color_distance(sample, color) < 10): #is near ghost color
                blocktype = Block['GHOST']
        for color in active:
            if(color_distance(sample, color) < 10): #is near active color
                blocktype = Block[strings[active.index(color)]]
        for color in blocks:
            if(color_distance(sample, color) < 15): #is near inactive color
                blocktype = Block['INACTIVE']
        if(color_distance(sample, emptyColor) < 15): #is near empty color
            blocktype = Block['EMPTY']
        if(color_distance(sample, textColor) < 25): #is near text color
            blocktype = Block['EMPTY']
        if(color_distance(sample, garbage) < 5):
            blocktype = Block['INACTIVE']
        if(blocktype != Block['UNKNOWN']): #at least one pixel is matched up, pack it up boys
            break
    if(blocktype == Block['UNKNOWN']): #no pixels were matched up
        blocktype = Block['EMPTY']
    return blocktype