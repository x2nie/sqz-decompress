import sqz
import math
from PIL import Image
from all_levels import *

LEVEL = 1

def decompress():
    compressed_file = "Assets/UNION.SQZ"
    output_file = "Assets/UNION.bin"
    bytes_copied = sqz.decompress(compressed_file, output_file)

    # with open('test_write.txt', 'r') as f:
    #     content_copied = f.read()

    # assert content_copied == content_to_copy

def drawtiles():
    f = open('Assets/UNION.bin', 'rb')
    f.seek(256+512)
    #? bitmaps
    BITMAP_COUNT = 32
    img = Image.new(mode="PA", size=(16*32, math.ceil(BITMAP_COUNT / 32)*16), color=0)
    img.putpalette(get_pil_palette(LEVEL), 'RGBA')
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
                img.putpixel([x*2+0, y], b1)
                img.putpixel([x*2+1, y], b2)
            print(line)
        print()

        # break
    # img.save('out.png', transparency=0)
    img = img.convert('RGBA')
    img.save('out.png')

if __name__ == '__main__':
    # decompress()
    # print(sqz.__doc__)
    # print(sqz.sqz.__doc__)

    drawtiles()