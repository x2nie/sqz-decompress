import sqz
import os, math
import png
from PIL import Image

filename = 'Tiled-Project/assets/tile-flag.png'
im = Image.open(filename)
px = im.load()

def get(X, Y):
    # Y = 2
    rows = []
    for y in range(16):
        row = []
        for x in range(16):
            row.append(px[X*16+x, Y*16+y])
        rows.append(row)
    return rows

def put(t, X, Y):
    global px
    for y in range(16):
        for x in range(16):
            z = t[y][x]
            if z == 0:
                continue
            px[X*16+x, Y*16+y] = z


# t1 = get(0, 3)
# put(t1, 1,4)
t = [
    get(0,2),
    get(1,2),
    get(5,2),
    get(6,2),
    get(7,2),
]

for z in range(0x1f): #? 5 bit, so far
    Y = z // 8
    X = z % 8
    for i in range(5):
        mask = 1 << i
        if z & mask > 0:
            put(t[i], X, 4+Y)

im.save(filename)