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

