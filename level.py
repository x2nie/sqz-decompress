import sqz
import os, math
import png
from struct import unpack
from all_levels import *

LEVEL = 1
# LEVEL = 2
# LEVEL = 3
# LEVEL = 4
# LEVEL = 5
# LEVEL = 6
# LEVEL = 7
# LEVEL = 8
# LEVEL = 9
# LEVEL = 10
# LEVEL = 11
# LEVEL = 14
# LEVEL = 15
# LEVEL = 16
HEIGHT = HEIGHTS[LEVEL-1]


def decompress():
    compressed_file = "Assets/LEVEL%s.SQZ" % LEVEL
    output_file = "Assets/LEVEL%s.bin" % LEVEL
    bytes_copied = sqz.decompress(compressed_file, output_file)

    # with open('test_write.txt', 'r') as f:
    #     content_copied = f.read()

    # assert content_copied == content_to_copy

def gen_Tiled():
    f = open('Assets/LEVEL%s.bin' % LEVEL, 'rb')

    #? find tile count
    BITMAP_COUNT = 0      #? init
    TABLE = []
    f.seek(256*HEIGHT) #skip
    for i in range(256):
        v = f.read(2)
        v = unpack('<H', v)[0]
        TABLE.append(v)
        if v < 256:
            BITMAP_COUNT = max(BITMAP_COUNT, v+1)
        print(v, end=', ')
    print()
    print('bitmap count=', BITMAP_COUNT)
    # BITMAP_COUNT=256
    W = 16*32 if BITMAP_COUNT >=32 else 16 * BITMAP_COUNT
    H = math.ceil(BITMAP_COUNT / 32)*16
    columns = W // 16

    #? get level-tiles props
    f.seek(-5029, os.SEEK_END)
    p1 = f.read(256)
    p2 = f.read(256)
    p3 = f.read(256)
    f.seek(-5029, os.SEEK_END)
    f.seek(4031, os.SEEK_CUR)
    p4 = f.read(256)

    #? TSX
    content = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<tileset version="1.10" tiledversion="1.10.2" name="level{LEVEL}" tilewidth="16" tileheight="16" tilecount="{BITMAP_COUNT}" columns="{columns}">',
        f' <image source="level{LEVEL}.png" width="{W}" height="{H}"/>',
        '</tileset>',
    ]
    with open('Tiled-Project/assets/level%s.tsx' % LEVEL, 'w') as tsx:
        for txt in content:
            print(txt, file=tsx)


    #? TMX

    content = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<map version="1.10" tiledversion="1.10.2" orientation="orthogonal" renderorder="right-down" width="256" height="{HEIGHT}" tilewidth="16" tileheight="16" infinite="0" nextlayerid="2" nextobjectid="1">',
        f' <tileset firstgid="1" source="assets/level{LEVEL}.tsx"/>',
         ' <tileset firstgid="257" source="assets/union.tsx"/>',
         ' <tileset firstgid="1000" source="assets/tile-flag.tsx"/>',
    ]

    #? MAIN tilemap
    content += [
        f' <layer id="1" name="LEVEL {LEVEL}" width="256" height="{HEIGHT}">',
         '  <data encoding="csv">',
    ]
    f.seek(0)
    for h in range(HEIGHT):
        row = []
        for x in range(256):
            v = f.read(1)[0]
            v = TABLE[v]
            v += 1
            row.append(str(v))
        line = ','.join(row)
        if h < HEIGHT -1: #? not the last
            line += ','
        content.append(line)
    content += [
        '</data>',
        ' </layer>',
    ]

    #? Tile Flag Byte 1 tilemap
    content += [
        f' <layer id="2" name="Horizontal Props" width="256" height="{HEIGHT}">',
         '  <data encoding="csv">',
    ]
    f.seek(0)
    for h in range(HEIGHT):
        row = []
        for x in range(256):
            v = f.read(1)[0]
            v = TABLE[v]
            if v >= 256:
                v = 0
            else:
                v = p1[v]
                v += 1000
            row.append(str(v))
        line = ','.join(row)
        if h < HEIGHT -1: #? not the last
            line += ','
        content.append(line)
    content += [
        '</data>',
        ' </layer>',
    ]

    #? Tile Flag Byte 2 tilemap
    content += [
        f' <layer id="3" name="Vertical Props" width="256" height="{HEIGHT}">',
         '  <data encoding="csv">',
    ]
    f.seek(0)
    for h in range(HEIGHT):
        row = []
        for x in range(256):
            v = f.read(1)[0]
            v = TABLE[v]
            if v >= 256:
                v = 0
            else:
                v = p2[v]
                v += 1008
            row.append(str(v))
        line = ','.join(row)
        if h < HEIGHT -1: #? not the last
            line += ','
        content.append(line)
    content += [
        '</data>',
        ' </layer>',
    ]

    #? Tile Flag Byte 3 tilemap
    content += [
        f' <layer id="3" name="Misc Props" width="256" height="{HEIGHT}">',
         '  <data encoding="csv">',
    ]
    f.seek(0)
    for h in range(HEIGHT):
        row = []
        for x in range(256):
            v = f.read(1)[0]
            v = TABLE[v]
            if v >= 256:
                v = 0
            else:
                v = p3[v]
                v += 1016
            row.append(str(v))
        line = ','.join(row)
        if h < HEIGHT -1: #? not the last
            line += ','
        content.append(line)
    content += [
        '</data>',
        ' </layer>',
    ]

    #? eof.map
    content += [
        '</map>',
    ]
    with open('Tiled-Project/map_level%s.tmx' % LEVEL, 'w') as tmx:
        for txt in content:
            print(txt, file=tmx)

    f.close()

def drawtiles():
    f = open('Assets/LEVEL%s.bin' % LEVEL, 'rb')
    # f.seek(128*15 + 256+512)
    BITMAP_COUNT = 0      #? init

    #? tilemap
    f.seek(256*HEIGHT) #skip

    #? lookup table
    for i in range(256):
        v = f.read(2)
        v = unpack('<H', v)[0]
        if v < 256:
            BITMAP_COUNT = max(BITMAP_COUNT, v+1)
        print(v, end=', ')
    print()
    print('bitmap count=', BITMAP_COUNT)
    # BITMAP_COUNT=256


    #? bitmaps    
    W = 16*32 if BITMAP_COUNT >=32 else 16 * BITMAP_COUNT
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
            # row = []
            line = ''
            for x in range(8):
                # v = int(f.read(1)[0])
                # v = int(f.read(1)[0])
                v = dst[i]; i +=1
                # row.append(v)

                b1 = v >> 4
                b2 = v & 0x0F
                # row.append(b1)
                # row.append(b2)

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

    with open('Tiled-Project/assets/level%s.png' % LEVEL, 'wb') as f:
        # https://stackoverflow.com/questions/62765455/convert-images-bit-depth-with-pypng
        png_writer = png.Writer(W, H, bitdepth=4, palette=get_png_palette(LEVEL))  # with palette
        png_writer.write(f, rows)

if __name__ == '__main__':
    # decompress()

    drawtiles()
    gen_Tiled()