PAL_INDEXS = [int(i) for i in '0134568899222298']    #? i.e. palette for level 2 is 1

#? Here is a table with the heights for each level:
#*          1   2    3   4   5    6    7    8   9    A   B   C   D   E   F    G
HEIGHTS = [ 49, 104, 49, 45, 128, 128, 128, 86, 110, 12, 24, 51, 51, 38, 173, 84]


def get_palette(level):
    from sty import fg, bg, ef, rs
    pal_index = PAL_INDEXS[level-1]
    result = []
    with open('PRE2.PAL', 'rb') as f:
        f.seek(4*16*pal_index)

        for i in range(16):
            # r = int(f.read(1)[0])
            # g = int(f.read(1)[0])
            # b = int(f.read(1)[0])
            # a = int(f.read(1)[0])
            # (a,b,g,r) = f.read(4)
            # (r,g,b,a) = f.read(4)
            (b,g,r,a) = f.read(4)
            result.append(bg(r, g, b) + '  ' + bg.rs)

    print('INUSED PALETTE:', ''.join(result))
    result[0] = '  '
    print('NoZero PALETTE:', ''.join(result))
    # for r in result:
    #     print(r)
    return result


def convert_planar_tile_4bpp(src, dst, dst_pitch):
    '''
    The format of a tile (and a sprite too) is 4-bit planar. I.e. for a 16*16
    image (like a tile) it goes like this:
    32 bytes of monochrome 16*16 bitmap for plane 0
    32 bytes of monochrome 16*16 bitmap for plane 1
    32 bytes of monochrome 16*16 bitmap for plane 2
    32 bytes of monochrome 16*16 bitmap for plane 3
    '''
    #* https://en.wikipedia.org/wiki/Planar_(computer_graphics)#Example
    tile_h = 16
    tile_w = 16
    plane_size = 16 * (16 // 8)
    for y in range(tile_h):
        for x in range(tile_w // 8):
            for i in range(8):
                mask = 1 << (7 - i)
                color = 0
                for b in range(4):
                    if src[b * plane_size] & mask:
                        color |= (1 << b)
                if i & 1:
                    dst[x * 4 + (i >> 1)] |= color
                else:
                    dst[x * 4 + (i >> 1)] = color << 4
            src += 1
        dst += dst_pitch