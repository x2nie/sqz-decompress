from struct import unpack
import sqz
from all_levels import *

#? this level consts:
LEVEL = 1
HEIGHT = HEIGHTS[LEVEL-1]
BITMAP_COUNT = 0      #? init

f = open('LEVEL%s.bin' % LEVEL, 'rb')

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

# a = f.read(2)

#? bitmaps
print('bitmap offset:', f.tell())
PAL = get_palette(LEVEL)
for b in range(BITMAP_COUNT):
    #?Draw a bitmap
    print('BITMAP #', b)
    buff = f.read(128)
    dst = sqz.convert_planar(buff)
    # print('buff:',type(buff),len(buff), buff)
    # print('dst:',type(dst), len(buff), dst)
    # break

    i = 0
    for y in range(16):
        line = ''
        for x in range(8):
            # v = int(f.read(1)[0])
            # v = int(f.read(1)[0])
            v = dst[i]; i +=1

            b1 = v >> 4
            b2 = v & 0x0F
            line += PAL[b1]
            line += PAL[b2]
        print(line)
    print()