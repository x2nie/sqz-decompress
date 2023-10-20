import sqz
import os, math
import png
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
    # f.seek(128*15 + 256+512)
    #? bitmaps
    f.seek(0, os.SEEK_END)
    BITMAP_COUNT = f.tell() // 128
    f.seek(0)

    W = 16*32
    H = math.ceil(BITMAP_COUNT / 32)*16
    # img = Image.new(mode="L", size=(W,H), color=0)
    # img.putpalette(get_pil_palette(LEVEL), 'RGBA')
    # print('bitmap offset:', f.tell())
    PAL = get_palette(LEVEL)
    rows = [[ 0 for x in range(W)] for y in range(H)]
    for b in range(BITMAP_COUNT):
        #?Draw a bitmap
        print('BITMAP #', b)
        buff = f.read(128)
        dst = sqz.convert_planar(buff)
        # print('buff:',type(buff),len(buff), buff)
        # print('dst:',type(dst), len(buff), dst)
        # break

        LEFT = b % 32
        TOP = b // 32

        i = 0
        for y in range(16):
            row = []
            line = ''
            for x in range(8):
                # v = int(f.read(1)[0])
                # v = int(f.read(1)[0])
                v = dst[i]; i +=1
                # row.append(v)

                b1 = v >> 4
                b2 = v & 0x0F
                row.append(b1)
                row.append(b2)

                rows[TOP*16+y][LEFT*16+x*2+0] = b1
                rows[TOP*16+y][LEFT*16+x*2+1] = b2
                

                line += PAL[b1]
                line += PAL[b2]
                # img.putpixel([x*2+0, y], b1)
                # img.putpixel([x*2+1, y], b2)
            # rows.append(row)
            print(line)
        print()

        # break
    # img.save('out.png', transparency=0)
    # img = img.convert('RGB')
    # img.save('out.png')

    # for r in rows:
    #     print('row:',r)

    with open('png-4bpp.png', 'wb') as f:
        #png_writer = png.Writer(im.shape[1], im.shape[0], bitdepth=4)  # without palette
        png_writer = png.Writer(W, H, bitdepth=4, palette=get_png_palette(LEVEL))  # with palette
        png_writer.write(f, rows)

if __name__ == '__main__':
    # decompress()
    # print(sqz.__doc__)
    # print(sqz.sqz.__doc__)

    drawtiles()