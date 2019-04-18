from PIL import Image

im = Image.open('reference.png')
pix = im.load()

#init values
startingX = 799
startingY = 108
deltaX = 33
deltaY = 33
startingX += int(deltaX/2)
startingY += int(deltaY/2)

#known colors
emptyColor = [9,9,9]
textColor = [85,89,88]

def color_distance(color, nextcolor): #get distance between 2 colors
    distance = abs(color[0] - nextcolor[0]) + abs(color[1] - nextcolor[1]) + abs(color[2] - nextcolor[2])
    return distance

for y in range(startingY, startingY + int(deltaY*20), int(deltaY)):
    for x in range(startingX, startingX + int(deltaX*10), int(deltaX)):
        emptySpaceFound = False
        for i in range(y - 5, y + 5):
            if(color_distance(pix[x,i], emptyColor) < 30 or color_distance(pix[x,i], textColor) < 30):
                emptySpaceFound = True
        if(emptySpaceFound):
            print(" ", end = "")
        else:
            print("x", end = "")
    print("")