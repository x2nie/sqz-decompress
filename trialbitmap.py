from struct import unpack
from all_levels import *

#? this level consts:
LEVEL = 1
HEIGHT = HEIGHTS[LEVEL-1]
BITMAP_COUNT = 0      #? init

f = open('LEVEL1.bin', 'rb')

#? tilemap
f.seek(256*HEIGHT) #skip

#? lookup table
for i in range(256):
    v = f.read(2)
    v = unpack('<H', v)[0]
    if v < 256:
        BITMAP_COUNT = max(BITMAP_COUNT, v)
    print(v, end=', ')
print()
print('bitmap count=', BITMAP_COUNT)


#? bitmaps
print('bitmap offset:', f.tell())
PAL = get_palette(LEVEL)
for b in range(13):
    #?Draw a bitmap
    print('BITMAP #', b)
    for y in range(16):
        line = ''
        for x in range(8):
            # v = int(f.read(1)[0])
            v = int(f.read(1)[0])
            b1 = v >> 4
            b2 = v & 0x0F
            line += PAL[b1]
            line += PAL[b2]
        print(line)
    print()